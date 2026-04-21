import uuid
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.market import MarketSegment, MarketStage
from app.models.startup import Startup
from app.models.valuation import (
    FlagType, MultipleAnalysis, OutlierFlag, ValuationDriver, ValuationEvent,
)
from app.schemas.valuation import (
    MultipleAnalysisRead, OutlierFlagRead, ValuationAnalysisResult,
    ValuationAnalyzeRequest, ValuationDriverRead, ValuationEventRead,
)
from app.models.shared import User
from app.services.auth import require_analyst
from app.services.valuation import analyze_valuation

router = APIRouter(prefix="/valuation", tags=["valuation"])


def _resolve_startup(db: Session, startup_name: str) -> Startup:
    startup = (
        db.query(Startup)
        .filter(func.lower(Startup.name) == startup_name.lower())
        .first()
    )
    if startup is None:
        raise HTTPException(
            status_code=404,
            detail=f"Startup '{startup_name}' no encontrada. Ver nombres en GET /startups/options",
        )
    return startup


def _resolve_segment(db: Session, sector: str, stage: str, geography: str) -> MarketSegment:
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


@router.get("/events", response_model=list[ValuationEventRead])
def list_valuation_events(
    startup_id: Optional[uuid.UUID] = Query(None, description="UUID de la startup. Ver IDs disponibles en GET /startups/options"),
    segment_id: Optional[uuid.UUID] = Query(None, description="UUID del segmento. Ver IDs disponibles en GET /market/segments/options"),
    db: Session = Depends(get_db),
):
    q = db.query(ValuationEvent)
    if startup_id is not None:
        q = q.filter(ValuationEvent.startup_id == startup_id)
    if segment_id is not None:
        q = q.filter(ValuationEvent.segment_id == segment_id)
    return q.order_by(ValuationEvent.date.desc()).all()


class _EventDetail(ValuationEventRead):
    multiple_analyses: list[MultipleAnalysisRead] = []


@router.get("/events/{event_id}", response_model=_EventDetail)
def get_valuation_event(
    event_id: uuid.UUID = Path(..., description="UUID del valuation event. Obtén IDs llamando GET /valuation/events"),
    db: Session = Depends(get_db),
):
    event = db.get(ValuationEvent, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="ValuationEvent no encontrado")
    analyses = (
        db.query(MultipleAnalysis)
        .filter(MultipleAnalysis.valuation_event_id == event_id)
        .all()
    )
    result = _EventDetail.model_validate(event)
    result.multiple_analyses = [MultipleAnalysisRead.model_validate(a) for a in analyses]
    return result


@router.post("/analyze", response_model=ValuationAnalysisResult)
def run_analysis(
    body: ValuationAnalyzeRequest,
    db: Session = Depends(get_db),
    _user: User = Depends(require_analyst),
):
    """Ejecuta análisis de valoración por nombre de startup y segmento legible.
    Ejemplo: startup_name='FinStack', segment_sector='Fintech', segment_stage='seed', segment_geography='LATAM'
    """
    startup = _resolve_startup(db, body.startup_name)
    segment = _resolve_segment(db, body.segment_sector, body.segment_stage, body.segment_geography)
    result = analyze_valuation(db, startup.id, segment.id)
    db.commit()
    return result


@router.get("/drivers/{startup_id}", response_model=list[ValuationDriverRead])
def list_drivers(
    startup_id: uuid.UUID = Path(..., description="UUID de la startup. Ver IDs disponibles en GET /startups/options"),
    db: Session = Depends(get_db),
):
    return (
        db.query(ValuationDriver)
        .filter(ValuationDriver.startup_id == startup_id)
        .all()
    )


@router.get("/outliers", response_model=list[OutlierFlagRead])
def list_outliers(
    flag_type: Optional[FlagType] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(OutlierFlag)
    if flag_type is not None:
        q = q.filter(OutlierFlag.flag_type == flag_type)
    return q.order_by(OutlierFlag.flagged_at.desc()).all()
