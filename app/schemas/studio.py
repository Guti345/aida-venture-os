import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.studio import BuildCostType, MilestoneType, StudioPhase, StudioSupportLevel


class StudioCompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    idea_date: Optional[date]
    validation_date: Optional[date]
    mvp_date: Optional[date]
    pmf_date: Optional[date]
    first_external_seed_date: Optional[date]
    build_cost_usd: float
    equity_retained_pct: Optional[float]
    studio_support_level: StudioSupportLevel
    current_studio_phase: StudioPhase
    notes: Optional[str]


class StudioCompanyWithStartup(StudioCompanyRead):
    startup_name: str = ""
    startup_sector: str = ""


class BuildCostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    studio_company_id: uuid.UUID
    cost_type: BuildCostType
    amount_usd: float
    period_date: date
    notes: Optional[str]


class StudioMilestoneRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    studio_company_id: uuid.UUID
    milestone_type: MilestoneType
    target_date: Optional[date]
    actual_date: Optional[date]
    achieved: bool
    notes: Optional[str]


class AlphaMetricRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    studio_company_id: uuid.UUID
    metric_name: str
    studio_value: float
    market_benchmark: Optional[float]
    delta_pct: Optional[float]
    is_alpha: Optional[bool]
    calculated_at: datetime


class StudioSummary(BaseModel):
    total_companies: int
    companies_by_phase: dict[str, int]
    total_build_cost_usd: float
    avg_build_cost_usd: float
    graduation_rate_pct: float
    avg_months_idea_to_mvp: Optional[float]
    alpha_vs_market: list[AlphaMetricRead]


class TimelineEvent(BaseModel):
    date: date
    event_type: str
    description: str
