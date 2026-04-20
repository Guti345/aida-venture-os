import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.fintech import (
    FintechComparable, FintechSubvertical, FintechUnitEconomics,
    ImpactLevel, RegulatoryComplexity, RegulatoryRisk, RegulatoryRiskStatus, RiskLevel,
)
from app.models.startup import MetricSnapshot, Startup
from app.schemas.fintech import (
    FintechComparableRead, FintechMarketOverview, FintechSubverticalRead,
    FintechSubverticalSummary, FintechUnitEconomicsRead, RegulatoryRiskRead,
)

router = APIRouter(prefix="/fintech", tags=["fintech"])


def _build_subvertical_summary(db: Session, sv: FintechSubvertical) -> FintechSubverticalSummary:
    # Startups en portafolio que tienen unit economics en este subvertical
    startup_ids_with_ue = (
        db.query(FintechUnitEconomics.startup_id)
        .filter(FintechUnitEconomics.subvertical_id == sv.id)
        .distinct()
        .all()
    )
    total_startups = len(startup_ids_with_ue)

    # ARR promedio: último snapshot ARR de cada startup vinculada al subvertical
    arr_values: list[float] = []
    for (startup_id,) in startup_ids_with_ue:
        snap = (
            db.query(MetricSnapshot)
            .filter(
                MetricSnapshot.startup_id == startup_id,
                MetricSnapshot.metric_name == "ARR",
            )
            .order_by(MetricSnapshot.period_date.desc())
            .first()
        )
        if snap is not None:
            arr_values.append(float(snap.value))

    avg_arr = round(sum(arr_values) / len(arr_values), 2) if arr_values else None

    comparables_count = (
        db.query(func.count(FintechComparable.id))
        .filter(FintechComparable.subvertical_id == sv.id)
        .scalar()
    )
    ue_count = (
        db.query(func.count(FintechUnitEconomics.id))
        .filter(FintechUnitEconomics.subvertical_id == sv.id)
        .scalar()
    )

    # Riesgos regulatorios: a través de startups vinculadas al subvertical
    reg_count = 0
    for (startup_id,) in startup_ids_with_ue:
        reg_count += (
            db.query(func.count(RegulatoryRisk.id))
            .filter(RegulatoryRisk.startup_id == startup_id)
            .scalar()
        )

    return FintechSubverticalSummary(
        subvertical=FintechSubverticalRead.model_validate(sv),
        total_startups_in_portfolio=total_startups,
        avg_arr_usd=avg_arr,
        comparables_count=comparables_count or 0,
        unit_economics_count=ue_count or 0,
        regulatory_risks_count=reg_count,
    )


@router.get("/subverticals/options", response_model=list[dict])
def subvertical_options(db: Session = Depends(get_db)):
    """Lista compacta de subverticales para usar como referencia de IDs en otros endpoints."""
    subverticals = db.query(FintechSubvertical).order_by(FintechSubvertical.name).all()
    return [
        {"id": str(sv.id), "name": sv.name, "risk_level": sv.risk_level.value}
        for sv in subverticals
    ]


@router.get("/subverticals", response_model=list[FintechSubverticalRead])
def list_subverticals(
    risk_level: Optional[RiskLevel] = Query(None),
    regulatory_complexity: Optional[RegulatoryComplexity] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(FintechSubvertical)
    if risk_level is not None:
        q = q.filter(FintechSubvertical.risk_level == risk_level)
    if regulatory_complexity is not None:
        q = q.filter(FintechSubvertical.regulatory_complexity == regulatory_complexity)
    return q.order_by(FintechSubvertical.name).all()


@router.get("/subverticals/{subvertical_id}", response_model=FintechSubverticalSummary)
def get_subvertical(
    subvertical_id: uuid.UUID = Path(..., description="UUID del subvertical. Ver IDs disponibles en GET /fintech/subverticals/options"),
    db: Session = Depends(get_db),
):
    sv = db.get(FintechSubvertical, subvertical_id)
    if sv is None:
        raise HTTPException(status_code=404, detail="Subvertical no encontrado")
    return _build_subvertical_summary(db, sv)


@router.get("/overview", response_model=FintechMarketOverview)
def fintech_overview(db: Session = Depends(get_db)):
    subverticals = db.query(FintechSubvertical).order_by(FintechSubvertical.name).all()

    summaries = [_build_subvertical_summary(db, sv) for sv in subverticals]

    # Subvertical con más startups en portafolio
    top = max(summaries, key=lambda s: s.total_startups_in_portfolio, default=None)
    top_name = top.subvertical.name if top else "N/A"

    # Inversión total LATAM: suma de valuation_usd de comparables con geography LATAM
    latam_total = (
        db.query(func.coalesce(func.sum(FintechComparable.valuation_usd), 0))
        .filter(FintechComparable.geography.ilike("%latam%"))
        .scalar()
    )

    return FintechMarketOverview(
        total_subverticals=len(subverticals),
        subverticals=summaries,
        top_subvertical_by_investment=top_name,
        latam_total_investment_usd=float(latam_total),
    )


@router.get("/unit-economics", response_model=list[FintechUnitEconomicsRead])
def list_unit_economics(
    startup_id: Optional[uuid.UUID] = Query(None, description="UUID de la startup. Ver IDs disponibles en GET /startups/options"),
    subvertical_id: Optional[uuid.UUID] = Query(None, description="UUID del subvertical. Ver IDs disponibles en GET /fintech/subverticals/options"),
    metric_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(FintechUnitEconomics)
    if startup_id is not None:
        q = q.filter(FintechUnitEconomics.startup_id == startup_id)
    if subvertical_id is not None:
        q = q.filter(FintechUnitEconomics.subvertical_id == subvertical_id)
    if metric_name is not None:
        q = q.filter(FintechUnitEconomics.metric_name.ilike(f"%{metric_name}%"))
    return q.order_by(FintechUnitEconomics.period_date.desc()).all()


@router.get("/comparables", response_model=list[FintechComparableRead])
def list_comparables(
    subvertical_id: Optional[uuid.UUID] = Query(None, description="UUID del subvertical. Ver IDs disponibles en GET /fintech/subverticals/options"),
    geography: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(FintechComparable)
    if subvertical_id is not None:
        q = q.filter(FintechComparable.subvertical_id == subvertical_id)
    if geography is not None:
        q = q.filter(FintechComparable.geography.ilike(f"%{geography}%"))
    return q.order_by(FintechComparable.comparable_name).all()


@router.get("/regulatory-risks", response_model=list[RegulatoryRiskRead])
def list_regulatory_risks(
    startup_id: Optional[uuid.UUID] = Query(None, description="UUID de la startup. Ver IDs disponibles en GET /startups/options"),
    country: Optional[str] = Query(None),
    impact_level: Optional[ImpactLevel] = Query(None),
    status: Optional[RegulatoryRiskStatus] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(RegulatoryRisk)
    if startup_id is not None:
        q = q.filter(RegulatoryRisk.startup_id == startup_id)
    if country is not None:
        q = q.filter(RegulatoryRisk.country == country.upper())
    if impact_level is not None:
        q = q.filter(RegulatoryRisk.impact_level == impact_level)
    if status is not None:
        q = q.filter(RegulatoryRisk.status == status)
    return q.order_by(RegulatoryRisk.impact_level, RegulatoryRisk.updated_at.desc()).all()
