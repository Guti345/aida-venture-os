import uuid
from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.market import MarketSegment, MarketStage
from app.models.shared import User
from app.models.startup import MetricSnapshot, Startup, StartupStage, StartupStatus
from app.schemas.market import PercentileResult
from app.schemas.startup import MetricIngestionForm, MetricIngestionResult, MetricSnapshotRead, StartupList, StartupRead, StartupWithMetrics
from app.services.auth import require_analyst
from app.services.importer import ingest_metrics
from app.services.percentile import calculate_percentile

router = APIRouter(prefix="/startups", tags=["startups"])


class MetricNameEnum(str, Enum):
    ARR = "ARR"
    MRR = "MRR"
    YoY_growth_pct = "YoY_growth_pct"
    burn_rate_monthly = "burn_rate_monthly"
    burn_multiple = "burn_multiple"
    runway_months = "runway_months"
    gross_margin_pct = "gross_margin_pct"
    active_customers = "active_customers"
    CAC = "CAC"
    LTV = "LTV"
    LTV_CAC_ratio = "LTV_CAC_ratio"
    NRR_pct = "NRR_pct"
    GRR_pct = "GRR_pct"
    CAC_payback_months = "CAC_payback_months"
    headcount = "headcount"
    NPL_rate_pct = "NPL_rate_pct"
    design_partners = "design_partners"
    waitlist_signups = "waitlist_signups"


def _get_startup_by_name(db: Session, startup_name: str) -> Startup:
    startup = (
        db.query(Startup)
        .filter(func.lower(Startup.name) == startup_name.lower())
        .first()
    )
    if startup is None:
        raise HTTPException(
            status_code=404,
            detail=f"Startup '{startup_name}' no encontrada. Ver nombres disponibles en GET /startups/options",
        )
    return startup


def _get_segment(db: Session, sector: str, stage: str, geography: str) -> MarketSegment:
    try:
        stage_enum = MarketStage(stage.lower())
    except ValueError:
        raise HTTPException(status_code=422, detail=f"segment_stage inválido: '{stage}'. Valores: {[e.value for e in MarketStage]}")
    seg = (
        db.query(MarketSegment)
        .filter(
            MarketSegment.sector.ilike(f"%{sector}%"),
            MarketSegment.stage == stage_enum,
            MarketSegment.geography.ilike(f"%{geography}%"),
        )
        .first()
    )
    if seg is None:
        raise HTTPException(
            status_code=404,
            detail=f"Segmento no encontrado para sector='{sector}', stage='{stage}', geography='{geography}'. Ver opciones en GET /market/segments/options",
        )
    return seg


@router.get("/options", response_model=list[dict])
def startup_options(db: Session = Depends(get_db)):
    """Lista compacta de startups para usar como referencia de nombres e IDs en otros endpoints."""
    startups = db.query(Startup).order_by(Startup.name).all()
    return [
        {"id": str(s.id), "name": s.name, "sector": s.sector, "stage": s.stage.value}
        for s in startups
    ]


@router.get("", response_model=list[StartupList])
def list_startups(
    name: Optional[str] = Query(None, description="Búsqueda parcial por nombre, e.g. 'Fin'"),
    sector: Optional[str] = Query(None),
    stage: Optional[StartupStage] = Query(None),
    country: Optional[str] = Query(None),
    studio_built: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Startup)

    if name is not None:
        q = q.filter(Startup.name.ilike(f"%{name}%"))
    if sector is not None:
        q = q.filter(Startup.sector.ilike(f"%{sector}%"))
    if stage is not None:
        q = q.filter(Startup.stage == stage)
    if country is not None:
        q = q.filter(Startup.country == country.upper())
    if studio_built is not None:
        q = q.filter(Startup.studio_built == studio_built)

    return q.order_by(Startup.name).all()


@router.get("/{startup_id}", response_model=StartupRead)
def get_startup(
    startup_id: uuid.UUID = Path(..., description="UUID de la startup. Ver IDs disponibles en GET /startups/options"),
    db: Session = Depends(get_db),
):
    startup = db.get(Startup, startup_id)
    if startup is None:
        raise HTTPException(status_code=404, detail="Startup no encontrada")
    return startup


@router.post("/ingest-metrics", response_model=MetricIngestionResult)
def ingest_metrics_endpoint(
    form: MetricIngestionForm,
    db: Session = Depends(get_db),
    _user: User = Depends(require_analyst),
):
    return ingest_metrics(db, form)


@router.get("/{startup_name}/metrics", response_model=list[MetricSnapshotRead])
def list_metrics(
    startup_name: str = Path(..., description="Nombre de la startup, e.g. 'FinStack'. Ver nombres en GET /startups/options"),
    metric_name: Optional[MetricNameEnum] = Query(None),
    db: Session = Depends(get_db),
):
    startup = _get_startup_by_name(db, startup_name)
    q = db.query(MetricSnapshot).filter(MetricSnapshot.startup_id == startup.id)
    if metric_name is not None:
        q = q.filter(MetricSnapshot.metric_name == metric_name.value)
    return q.order_by(desc(MetricSnapshot.period_date)).all()


@router.get("/{startup_name}/percentile", response_model=PercentileResult)
def get_percentile(
    startup_name: str = Path(..., description="Nombre de la startup, e.g. 'FinStack'. Ver nombres en GET /startups/options"),
    metric_name: MetricNameEnum = Query(...),
    segment_sector: str = Query(..., description="Sector del segmento, e.g. 'Fintech'"),
    segment_stage: str = Query(..., description="Etapa del segmento: pre_seed, seed, series_a, series_b"),
    segment_geography: str = Query(default="LATAM", description="Geografía del segmento, e.g. 'LATAM'"),
    db: Session = Depends(get_db),
):
    startup = _get_startup_by_name(db, startup_name)
    segment = _get_segment(db, segment_sector, segment_stage, segment_geography)
    return calculate_percentile(db, startup.id, metric_name.value, segment.id)


@router.get("/{startup_name}/metrics/latest", response_model=dict[str, MetricSnapshotRead])
def latest_metrics(
    startup_name: str = Path(..., description="Nombre de la startup, e.g. 'FinStack'. Ver nombres en GET /startups/options"),
    db: Session = Depends(get_db),
):
    startup = _get_startup_by_name(db, startup_name)
    rows = (
        db.query(MetricSnapshot)
        .filter(MetricSnapshot.startup_id == startup.id)
        .order_by(desc(MetricSnapshot.period_date))
        .all()
    )
    latest: dict[str, MetricSnapshot] = {}
    for row in rows:
        if row.metric_name not in latest:
            latest[row.metric_name] = row
    return latest
