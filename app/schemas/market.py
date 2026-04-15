import uuid
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.market import MarketStage, MultipleType


class MarketSegmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sector: str
    subsector: Optional[str]
    stage: MarketStage
    geography: Optional[str]
    country: Optional[str]
    created_at: datetime


class BenchmarkEntryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    segment_id: uuid.UUID
    multiple_type: MultipleType
    p10: Optional[float]
    p25: Optional[float]
    p50: Optional[float]
    p75: Optional[float]
    p90: Optional[float]
    reference_date: date
    source: str
    notes: Optional[str]


class PercentileResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    startup_id: uuid.UUID
    metric_name: str
    value: float
    p25: float
    p50: float
    p75: float
    p90: float
    percentile_position: float = Field(..., ge=0.0, le=100.0)
    verdict: Literal["top_performer", "above_median", "below_median", "underperformer"]
