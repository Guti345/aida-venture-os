import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.valuation import ValuationVerdict, DriverType, FlagType


class ValuationEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    round_id: Optional[uuid.UUID]
    pre_money_val: float
    arr_at_time: Optional[float]
    multiple_paid: Optional[float]
    segment_id: Optional[uuid.UUID]
    date: date


class MultipleAnalysisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    valuation_event_id: uuid.UUID
    segment_id: uuid.UUID
    multiple_paid: float
    market_p25: float
    market_p50: float
    market_p75: float
    premium_pct: Optional[float]
    verdict: ValuationVerdict
    justification: Optional[str]


class ValuationAnalysisResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event: ValuationEventRead
    analysis: MultipleAnalysisRead
    entry_discipline_summary: str


class ValuationDriverRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    driver_type: DriverType
    value: float
    benchmark_threshold: Optional[float]
    above_threshold: bool
    premium_justified: bool
    notes: Optional[str]


class OutlierFlagRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    metric_name: str
    value: float
    market_p25: Optional[float]
    market_p75: Optional[float]
    flag_type: FlagType
    flagged_at: datetime
