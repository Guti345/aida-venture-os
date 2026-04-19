import uuid
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.dealflow import (
    DDChecklist, DDItemStatus, DealOpportunity, DealStatus,
    ICMemo, SourcingChannel, ThesisAlignment,
)
from app.schemas.dealflow import (
    DDChecklistRead, DealDetailRead, DealOpportunityWithStartup,
    DealSummary, ICMemoRead, SourcingChannelRead, ThesisAlignmentRead,
)

router_deals = APIRouter(prefix="/deals", tags=["dealflow"])
router_sourcing = APIRouter(prefix="/sourcing", tags=["dealflow"])


def _enrich_deal(deal: DealOpportunity) -> DealOpportunityWithStartup:
    obj = DealOpportunityWithStartup.model_validate(deal)
    if deal.startup is not None:
        obj.startup_name = deal.startup.name
    if deal.sourcing_channel is not None:
        obj.sourcing_channel_name = deal.sourcing_channel.name
    return obj


def _get_deal_or_404(db: Session, deal_id: uuid.UUID) -> DealOpportunity:
    deal = (
        db.query(DealOpportunity)
        .options(
            joinedload(DealOpportunity.startup),
            joinedload(DealOpportunity.sourcing_channel),
            joinedload(DealOpportunity.thesis_alignments),
            joinedload(DealOpportunity.dd_checklists),
            joinedload(DealOpportunity.ic_memos),
        )
        .filter(DealOpportunity.id == deal_id)
        .first()
    )
    if deal is None:
        raise HTTPException(status_code=404, detail="Deal no encontrado")
    return deal


# ── /deals ────────────────────────────────────────────────────────────────────

@router_deals.get("", response_model=list[DealOpportunityWithStartup])
def list_deals(
    status: Optional[str] = Query(None),
    sourcing_channel_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db),
):
    q = (
        db.query(DealOpportunity)
        .options(
            joinedload(DealOpportunity.startup),
            joinedload(DealOpportunity.sourcing_channel),
        )
    )
    if status is not None:
        try:
            status_enum = DealStatus(status.lower())
        except ValueError:
            raise HTTPException(status_code=422, detail=f"status inválido: '{status}'")
        q = q.filter(DealOpportunity.status == status_enum)
    if sourcing_channel_id is not None:
        q = q.filter(DealOpportunity.sourcing_channel_id == sourcing_channel_id)

    deals = q.order_by(DealOpportunity.identified_at.desc()).all()
    return [_enrich_deal(d) for d in deals]


@router_deals.get("/summary", response_model=DealSummary)
def deals_summary(db: Session = Depends(get_db)):
    deals = db.query(DealOpportunity).all()
    total = len(deals)

    by_status: dict[str, int] = {}
    for d in deals:
        key = d.status.value
        by_status[key] = by_status.get(key, 0) + 1

    # Score promedio de thesis (suma(score) / suma(max_score) * 10)
    rows = db.query(ThesisAlignment.score, ThesisAlignment.max_score).all()
    if rows:
        total_score = sum(r.score for r in rows)
        total_max = sum(r.max_score for r in rows)
        avg_thesis = round(total_score / total_max * 10, 2) if total_max > 0 else None
    else:
        avg_thesis = None

    # Deals identificados en el mes en curso
    today = date.today()
    this_month = sum(
        1 for d in deals
        if d.identified_at.year == today.year and d.identified_at.month == today.month
    )

    return DealSummary(
        total_deals=total,
        deals_by_status=by_status,
        avg_thesis_score=avg_thesis,
        deals_this_month=this_month,
    )


@router_deals.get("/{deal_id}", response_model=DealDetailRead)
def get_deal(deal_id: uuid.UUID, db: Session = Depends(get_db)):
    deal = _get_deal_or_404(db, deal_id)
    return DealDetailRead(
        deal=_enrich_deal(deal),
        thesis_alignments=[ThesisAlignmentRead.model_validate(t) for t in deal.thesis_alignments],
        dd_checklist=[DDChecklistRead.model_validate(c) for c in deal.dd_checklists],
        ic_memos=[ICMemoRead.model_validate(m) for m in sorted(deal.ic_memos, key=lambda m: m.version, reverse=True)],
    )


@router_deals.get("/{deal_id}/thesis", response_model=dict)
def deal_thesis(deal_id: uuid.UUID, db: Session = Depends(get_db)):
    deal = _get_deal_or_404(db, deal_id)
    alignments = [ThesisAlignmentRead.model_validate(t) for t in deal.thesis_alignments]

    total_score = sum(a.score for a in alignments)
    total_max = sum(a.max_score for a in alignments)
    pct = round(total_score / total_max * 100, 1) if total_max > 0 else None

    return {
        "deal_id": deal_id,
        "alignments": alignments,
        "total_score": total_score,
        "total_max_score": total_max,
        "thesis_score_pct": pct,
    }


@router_deals.get("/{deal_id}/checklist", response_model=dict)
def deal_checklist(deal_id: uuid.UUID, db: Session = Depends(get_db)):
    deal = _get_deal_or_404(db, deal_id)
    items = [DDChecklistRead.model_validate(c) for c in deal.dd_checklists]

    # Progreso por categoría
    by_category: dict[str, dict] = {}
    for item in items:
        cat = item.item_category.value
        if cat not in by_category:
            by_category[cat] = {"total": 0, "done": 0, "in_progress": 0, "pending": 0}
        by_category[cat]["total"] += 1
        if item.status == DDItemStatus.done:
            by_category[cat]["done"] += 1
        elif item.status == DDItemStatus.in_progress:
            by_category[cat]["in_progress"] += 1
        else:
            by_category[cat]["pending"] += 1

    for cat, counts in by_category.items():
        t = counts["total"]
        counts["pct_done"] = round(counts["done"] / t * 100, 1) if t > 0 else 0.0

    total = len(items)
    total_done = sum(1 for i in items if i.status == DDItemStatus.done)
    overall_pct = round(total_done / total * 100, 1) if total > 0 else 0.0

    return {
        "deal_id": deal_id,
        "items": items,
        "total_items": total,
        "total_done": total_done,
        "overall_pct_done": overall_pct,
        "by_category": by_category,
    }


@router_deals.get("/{deal_id}/memos", response_model=list[ICMemoRead])
def deal_memos(deal_id: uuid.UUID, db: Session = Depends(get_db)):
    deal = _get_deal_or_404(db, deal_id)
    return sorted(
        [ICMemoRead.model_validate(m) for m in deal.ic_memos],
        key=lambda m: m.version,
        reverse=True,
    )


# ── /sourcing ─────────────────────────────────────────────────────────────────

@router_sourcing.get("/channels", response_model=list[SourcingChannelRead])
def list_channels(db: Session = Depends(get_db)):
    return (
        db.query(SourcingChannel)
        .filter(SourcingChannel.active.is_(True))
        .order_by(SourcingChannel.name)
        .all()
    )


@router_sourcing.get("/channels/{channel_id}/deals", response_model=list[DealOpportunityWithStartup])
def channel_deals(channel_id: uuid.UUID, db: Session = Depends(get_db)):
    channel = db.get(SourcingChannel, channel_id)
    if channel is None:
        raise HTTPException(status_code=404, detail="Canal de sourcing no encontrado")

    deals = (
        db.query(DealOpportunity)
        .options(
            joinedload(DealOpportunity.startup),
            joinedload(DealOpportunity.sourcing_channel),
        )
        .filter(DealOpportunity.sourcing_channel_id == channel_id)
        .order_by(DealOpportunity.identified_at.desc())
        .all()
    )
    return [_enrich_deal(d) for d in deals]
