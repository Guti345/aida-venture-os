import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.startup import PeriodType, StartupStage, StartupStatus


class StartupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    sector: str
    subsector: Optional[str]
    stage: StartupStage
    geography: Optional[str]
    country: Optional[str]
    city: Optional[str]
    founded_at: Optional[date]
    studio_built: bool
    website: Optional[str]
    description: Optional[str]
    status: StartupStatus
    is_simulated: bool
    created_at: datetime


class StartupList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    sector: str
    stage: StartupStage
    country: Optional[str]
    status: StartupStatus
    is_simulated: bool


class MetricSnapshotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    metric_name: str
    value: float
    unit: Optional[str]
    currency: Optional[str]
    period_date: date
    period_type: PeriodType
    source: str
    notes: Optional[str]


class MetricSnapshotCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    startup_id: uuid.UUID
    metric_name: str
    value: float
    unit: Optional[str] = None
    currency: Optional[str] = None
    period_date: date
    period_type: PeriodType
    source: str
    notes: Optional[str] = None


class StartupWithMetrics(StartupRead):
    metrics: list[MetricSnapshotRead] = []
