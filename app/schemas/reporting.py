import uuid
from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.models.reporting import ICDecisionType, LPTier, ReportingFrequency, ReportStatus, ReportType


class LPProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lp_id: uuid.UUID
    preferred_metrics_json: Optional[dict[str, Any]]
    reporting_frequency: ReportingFrequency
    tier: LPTier
    last_update_at: datetime


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    report_type: ReportType
    title: str
    fund_id: uuid.UUID
    generated_at: datetime
    status: ReportStatus
    content_json: Optional[dict[str, Any]]


class NarrativeBlockRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    report_id: uuid.UUID
    section_name: str
    content_text: str
    data_references_json: Optional[dict[str, Any]]
    order_index: int


class ICDecisionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    deal_id: uuid.UUID
    decision: ICDecisionType
    decision_date: date
    committee_members_json: Optional[dict[str, Any]]
    rationale: Optional[str]
    data_snapshot_json: Optional[dict[str, Any]]


class LPReportSummary(BaseModel):
    fund_name: str
    report_date: date
    total_invested_usd: float
    portfolio_companies: int
    active_companies: int
    studio_companies: int
    top_performers: list[str]
    fund_moic_current: Optional[float]
    fund_irr_current: Optional[float]
    deals_in_pipeline: int
    deals_invested_this_year: int
    studio_graduation_rate_pct: float
    narrative_summary: str


class PortfolioSnapshotItem(BaseModel):
    startup_name: str
    sector: str
    stage: str
    country: Optional[str]
    arr_usd: Optional[float]
    mrr_usd: Optional[float]
    yoy_growth_pct: Optional[float]
    burn_multiple: Optional[float]
    runway_months: Optional[float]
    nrr_pct: Optional[float]
    status: str
