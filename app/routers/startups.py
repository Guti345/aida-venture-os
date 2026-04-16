import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.startup import MetricSnapshot, Startup, StartupStage, StartupStatus
from app.schemas.startup import MetricSnapshotRead, StartupList, StartupRead, StartupWithMetrics

router = APIRouter(prefix="/startups", tags=["startups"])


@router.get("", response_model=list[StartupList])
def list_startups(
    sector: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    studio_built: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Startup)

    if sector is not None:
        q = q.filter(Startup.sector.ilike(f"%{sector}%"))
    if stage is not None:
        try:
            stage_enum = StartupStage(stage.lower())
        except ValueError:
            raise HTTPException(status_code=422, detail=f"stage inválido: '{stage}'")
        q = q.filter(Startup.stage == stage_enum)
    if country is not None:
        q = q.filter(Startup.country == country.upper())
    if studio_built is not None:
        q = q.filter(Startup.studio_built == studio_built)

    return q.order_by(Startup.name).all()


@router.get("/{startup_id}", response_model=StartupRead)
def get_startup(startup_id: uuid.UUID, db: Session = Depends(get_db)):
    startup = db.get(Startup, startup_id)
    if startup is None:
        raise HTTPException(status_code=404, detail="Startup no encontrada")
    return startup


@router.get("/{startup_id}/metrics", response_model=list[MetricSnapshotRead])
def list_metrics(
    startup_id: uuid.UUID,
    metric_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    if db.get(Startup, startup_id) is None:
        raise HTTPException(status_code=404, detail="Startup no encontrada")

    q = db.query(MetricSnapshot).filter(MetricSnapshot.startup_id == startup_id)

    if metric_name is not None:
        q = q.filter(MetricSnapshot.metric_name == metric_name)

    return q.order_by(desc(MetricSnapshot.period_date)).all()


@router.get("/{startup_id}/metrics/latest", response_model=dict[str, MetricSnapshotRead])
def latest_metrics(startup_id: uuid.UUID, db: Session = Depends(get_db)):
    if db.get(Startup, startup_id) is None:
        raise HTTPException(status_code=404, detail="Startup no encontrada")

    rows = (
        db.query(MetricSnapshot)
        .filter(MetricSnapshot.startup_id == startup_id)
        .order_by(desc(MetricSnapshot.period_date))
        .all()
    )

    latest: dict[str, MetricSnapshot] = {}
    for row in rows:
        if row.metric_name not in latest:
            latest[row.metric_name] = row

    return latest
