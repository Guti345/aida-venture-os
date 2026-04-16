import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.market import BenchmarkEntry, MarketSegment, MarketStage, MultipleType
from app.schemas.market import BenchmarkEntryRead, MarketSegmentRead

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/segments", response_model=list[MarketSegmentRead])
def list_segments(
    sector: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),
    geography: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(MarketSegment)

    if sector is not None:
        q = q.filter(MarketSegment.sector.ilike(f"%{sector}%"))
    if stage is not None:
        try:
            stage_enum = MarketStage(stage.lower())
        except ValueError:
            raise HTTPException(status_code=422, detail=f"stage inválido: '{stage}'")
        q = q.filter(MarketSegment.stage == stage_enum)
    if geography is not None:
        q = q.filter(MarketSegment.geography.ilike(f"%{geography}%"))
    if country is not None:
        q = q.filter(MarketSegment.country == country.upper())

    return q.order_by(MarketSegment.sector, MarketSegment.stage).all()


@router.get("/benchmarks", response_model=list[BenchmarkEntryRead])
def list_benchmarks(
    segment_id: Optional[uuid.UUID] = Query(None),
    multiple_type: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(BenchmarkEntry).join(
        MarketSegment, BenchmarkEntry.segment_id == MarketSegment.id
    )

    if segment_id is not None:
        q = q.filter(BenchmarkEntry.segment_id == segment_id)
    if multiple_type is not None:
        try:
            multiple_type_enum = MultipleType(multiple_type.upper())
        except ValueError:
            raise HTTPException(status_code=422, detail=f"multiple_type inválido: '{multiple_type}'")
        q = q.filter(BenchmarkEntry.multiple_type == multiple_type_enum)
    if sector is not None:
        q = q.filter(MarketSegment.sector.ilike(f"%{sector}%"))

    return q.order_by(desc(BenchmarkEntry.reference_date)).all()
