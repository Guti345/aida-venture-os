from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.dealflow import DealOpportunity, DealStatus
from app.models.reporting import ICDecision
from app.schemas.reporting import ICDecisionRead, LPReportSummary, PortfolioSnapshotItem
from app.models.shared import User
from app.services.auth import require_analyst
from app.services.reporter import generate_lp_report, get_portfolio_snapshot

router = APIRouter(prefix="/reports", tags=["reporting"])


@router.get("/lp-summary", response_model=LPReportSummary)
def lp_summary(db: Session = Depends(get_db), _user: User = Depends(require_analyst)):
    return generate_lp_report(db)


@router.get("/portfolio-snapshot", response_model=list[PortfolioSnapshotItem])
def portfolio_snapshot(db: Session = Depends(get_db)):
    return get_portfolio_snapshot(db)


@router.get("/ic-decisions", response_model=list[ICDecisionRead])
def ic_decisions(db: Session = Depends(get_db)):
    return (
        db.query(ICDecision)
        .order_by(desc(ICDecision.decision_date))
        .all()
    )


@router.get("/pipeline-status")
def pipeline_status(db: Session = Depends(get_db)):
    deals = (
        db.query(DealOpportunity)
        .options(
            joinedload(DealOpportunity.startup),
            joinedload(DealOpportunity.sourcing_channel),
        )
        .order_by(DealOpportunity.identified_at.desc())
        .all()
    )

    active_statuses = {DealStatus.identified, DealStatus.screening, DealStatus.dd, DealStatus.ic}

    pipeline = []
    for d in deals:
        if d.status not in active_statuses:
            continue
        pipeline.append({
            "deal_id": str(d.id),
            "startup_name": d.startup.name if d.startup else None,
            "status": d.status.value,
            "sourcing_channel": d.sourcing_channel.name if d.sourcing_channel else None,
            "identified_at": d.identified_at.isoformat(),
            "days_in_pipeline": (
                (__import__("datetime").date.today() - d.identified_at).days
            ),
            "decision_notes": d.decision_notes,
        })

    by_status: dict[str, int] = {}
    for item in pipeline:
        s = item["status"]
        by_status[s] = by_status.get(s, 0) + 1

    return {
        "total_active": len(pipeline),
        "by_status": by_status,
        "deals": pipeline,
    }
