import uuid
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.valuation import (
    FlagType, MultipleAnalysis, OutlierFlag, ValuationDriver, ValuationEvent,
)
from app.schemas.valuation import (
    MultipleAnalysisRead, OutlierFlagRead, ValuationAnalysisResult,
    ValuationDriverRead, ValuationEventRead,
)
from app.services.valuation import analyze_valuation

router = APIRouter(prefix="/valuation", tags=["valuation"])


@router.get("/events", response_model=list[ValuationEventRead])
def list_valuation_events(
    startup_id: Optional[uuid.UUID] = Query(None),
    segment_id: Optional[uuid.UUID] = Query(None),
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
def get_valuation_event(event_id: uuid.UUID, db: Session = Depends(get_db)):
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
    startup_id: uuid.UUID = Body(..., embed=True),
    segment_id: uuid.UUID = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    result = analyze_valuation(db, startup_id, segment_id)
    db.commit()
    return result


@router.get("/drivers/{startup_id}", response_model=list[ValuationDriverRead])
def list_drivers(startup_id: uuid.UUID, db: Session = Depends(get_db)):
    return (
        db.query(ValuationDriver)
        .filter(ValuationDriver.startup_id == startup_id)
        .all()
    )


@router.get("/outliers", response_model=list[OutlierFlagRead])
def list_outliers(
    flag_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(OutlierFlag)
    if flag_type is not None:
        try:
            flag_enum = FlagType(flag_type.lower())
        except ValueError:
            raise HTTPException(status_code=422, detail=f"flag_type inválido: '{flag_type}'")
        q = q.filter(OutlierFlag.flag_type == flag_enum)
    return q.order_by(OutlierFlag.flagged_at.desc()).all()
