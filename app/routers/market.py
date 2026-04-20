import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.market import BenchmarkEntry, MarketSegment, MarketStage, MultipleType
from app.schemas.market import BenchmarkEntryRead, MarketSegmentRead

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/segments/options", response_model=list[dict])
def segment_options(db: Session = Depends(get_db)):
    """Lista compacta de segmentos para usar como referencia de IDs en /percentile y /valuation/analyze."""
    segments = db.query(MarketSegment).order_by(MarketSegment.sector, MarketSegment.stage).all()
    return [
        {
            "id": str(s.id),
            "sector": s.sector,
            "subsector": s.subsector,
            "stage": s.stage.value,
            "geography": s.geography,
        }
        for s in segments
    ]


@router.get("/segments", response_model=list[MarketSegmentRead])
def list_segments(
    sector: Optional[str] = Query(None),
    stage: Optional[MarketStage] = Query(None),
    geography: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(MarketSegment)

    if sector is not None:
        q = q.filter(MarketSegment.sector.ilike(f"%{sector}%"))
    if stage is not None:
        q = q.filter(MarketSegment.stage == stage)
    if geography is not None:
        q = q.filter(MarketSegment.geography.ilike(f"%{geography}%"))
    if country is not None:
        q = q.filter(MarketSegment.country == country.upper())

    return q.order_by(MarketSegment.sector, MarketSegment.stage).all()


@router.get("/benchmarks", response_model=list[BenchmarkEntryRead])
def list_benchmarks(
    segment_id: Optional[uuid.UUID] = Query(None, description="UUID del segmento. Ver IDs disponibles en GET /market/segments/options"),
    multiple_type: Optional[MultipleType] = Query(None),
    sector: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(BenchmarkEntry).join(
        MarketSegment, BenchmarkEntry.segment_id == MarketSegment.id
    )

    if segment_id is not None:
        q = q.filter(BenchmarkEntry.segment_id == segment_id)
    if multiple_type is not None:
        q = q.filter(BenchmarkEntry.multiple_type == multiple_type)
    if sector is not None:
        q = q.filter(MarketSegment.sector.ilike(f"%{sector}%"))

    return q.order_by(desc(BenchmarkEntry.reference_date)).all()
