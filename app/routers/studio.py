import uuid

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.studio import AlphaMetric, BuildCost, StudioCompany, StudioMilestone
from app.schemas.studio import (
    AlphaMetricRead, BuildCostRead, StudioCompanyRead, StudioCompanyWithStartup,
    StudioMilestoneRead, StudioSummary, TimelineEvent,
)
from app.services.alpha import calculate_alpha_score, get_company_timeline, get_studio_summary

router = APIRouter(prefix="/studio", tags=["studio"])


def _get_sc_or_404(db: Session, studio_company_id: uuid.UUID) -> StudioCompany:
    sc = db.get(StudioCompany, studio_company_id)
    if sc is None:
        raise HTTPException(status_code=404, detail="StudioCompany no encontrada")
    return sc


@router.get("/summary", response_model=StudioSummary)
def studio_summary(db: Session = Depends(get_db)):
    return get_studio_summary(db)


@router.get("/companies/options", response_model=list[dict])
def company_options(db: Session = Depends(get_db)):
    """Lista compacta de empresas del studio para usar como referencia de IDs en otros endpoints."""
    companies = (
        db.query(StudioCompany)
        .options(joinedload(StudioCompany.startup))
        .order_by(StudioCompany.current_studio_phase)
        .all()
    )
    return [
        {
            "id": str(sc.id),
            "startup_name": sc.startup.name if sc.startup else None,
            "current_studio_phase": sc.current_studio_phase.value,
        }
        for sc in companies
    ]


@router.get("/companies", response_model=list[StudioCompanyWithStartup])
def list_companies(db: Session = Depends(get_db)):
    companies = (
        db.query(StudioCompany)
        .options(joinedload(StudioCompany.startup))
        .order_by(StudioCompany.current_studio_phase)
        .all()
    )
    results = []
    for sc in companies:
        obj = StudioCompanyWithStartup.model_validate(sc)
        if sc.startup:
            obj.startup_name = sc.startup.name
            obj.startup_sector = sc.startup.sector or ""
        results.append(obj)
    return results


@router.get("/companies/{studio_company_id}", response_model=StudioCompanyWithStartup)
def get_company(
    studio_company_id: uuid.UUID = Path(..., description="UUID de la empresa del studio. Ver IDs disponibles en GET /studio/companies/options"),
    db: Session = Depends(get_db),
):
    sc = (
        db.query(StudioCompany)
        .options(joinedload(StudioCompany.startup))
        .filter(StudioCompany.id == studio_company_id)
        .first()
    )
    if sc is None:
        raise HTTPException(status_code=404, detail="StudioCompany no encontrada")
    obj = StudioCompanyWithStartup.model_validate(sc)
    if sc.startup:
        obj.startup_name = sc.startup.name
        obj.startup_sector = sc.startup.sector or ""
    return obj


@router.get("/companies/{studio_company_id}/timeline", response_model=list[TimelineEvent])
def company_timeline(
    studio_company_id: uuid.UUID = Path(..., description="UUID de la empresa del studio. Ver IDs disponibles en GET /studio/companies/options"),
    db: Session = Depends(get_db),
):
    return get_company_timeline(db, studio_company_id)


@router.get("/companies/{studio_company_id}/costs", response_model=list[BuildCostRead])
def company_costs(
    studio_company_id: uuid.UUID = Path(..., description="UUID de la empresa del studio. Ver IDs disponibles en GET /studio/companies/options"),
    db: Session = Depends(get_db),
):
    _get_sc_or_404(db, studio_company_id)
    return (
        db.query(BuildCost)
        .filter(BuildCost.studio_company_id == studio_company_id)
        .order_by(BuildCost.period_date)
        .all()
    )


@router.get("/companies/{studio_company_id}/milestones", response_model=list[StudioMilestoneRead])
def company_milestones(
    studio_company_id: uuid.UUID = Path(..., description="UUID de la empresa del studio. Ver IDs disponibles en GET /studio/companies/options"),
    db: Session = Depends(get_db),
):
    _get_sc_or_404(db, studio_company_id)
    return (
        db.query(StudioMilestone)
        .filter(StudioMilestone.studio_company_id == studio_company_id)
        .order_by(StudioMilestone.actual_date.nulls_last(), StudioMilestone.target_date)
        .all()
    )


@router.get("/alpha", response_model=list[AlphaMetricRead])
def list_alpha_metrics(db: Session = Depends(get_db)):
    return (
        db.query(AlphaMetric)
        .filter(AlphaMetric.is_alpha.is_(True))
        .order_by(AlphaMetric.delta_pct.desc())
        .all()
    )


@router.get("/alpha/score/{studio_company_id}")
def alpha_score(
    studio_company_id: uuid.UUID = Path(..., description="UUID de la empresa del studio. Ver IDs disponibles en GET /studio/companies/options"),
    db: Session = Depends(get_db),
):
    return calculate_alpha_score(db, studio_company_id)
