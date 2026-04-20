import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.market import BenchmarkEntry, MarketSegment, MarketStage, MultipleType
from app.schemas.market import BenchmarkEntryRead, MarketSegmentRead

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/segments/options", response_model=list[dict])
def segment_options(db: Session = Depends(get_db)):
    """Lista compacta de segmentos para usar como referencia en /percentile y /valuation/analyze."""
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
    sector: Optional[str] = Query(None, description="Sector del segmento, e.g. 'Fintech'. Combinado con stage resuelve el segmento automáticamente."),
    stage: Optional[MarketStage] = Query(None, description="Etapa del segmento. Combinada con sector resuelve el segmento automáticamente."),
    geography: str = Query(default="LATAM", description="Geografía del segmento para resolución automática"),
    multiple_type: Optional[MultipleType] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(BenchmarkEntry).join(
        MarketSegment, BenchmarkEntry.segment_id == MarketSegment.id
    )

    if sector is not None and stage is not None:
        # Resolve segment by human-readable fields
        segment = (
            db.query(MarketSegment)
            .filter(
                MarketSegment.sector.ilike(f"%{sector}%"),
                MarketSegment.stage == stage,
                MarketSegment.geography.ilike(f"%{geography}%"),
            )
            .first()
        )
        if segment is None:
            raise HTTPException(
                status_code=404,
                detail=f"Segmento no encontrado para sector='{sector}', stage='{stage.value}', geography='{geography}'. Ver opciones en GET /market/segments/options",
            )
        q = q.filter(BenchmarkEntry.segment_id == segment.id)
    elif sector is not None:
        q = q.filter(MarketSegment.sector.ilike(f"%{sector}%"))

    if multiple_type is not None:
        q = q.filter(BenchmarkEntry.multiple_type == multiple_type)

    return q.order_by(desc(BenchmarkEntry.reference_date)).all()
