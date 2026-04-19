import uuid
from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.models.fintech import ImpactLevel, RegulatoryComplexity, RegulatoryRiskStatus, RiskLevel


class FintechSubverticalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: Optional[str]
    risk_level: RiskLevel
    regulatory_complexity: RegulatoryComplexity
    key_metrics_json: Optional[dict[str, Any]]


class FintechUnitEconomicsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    subvertical_id: Optional[uuid.UUID]
    metric_name: str
    value: float
    unit: Optional[str]
    period_date: date
    notes: Optional[str]


class RegulatoryRiskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    country: str
    risk_type: str
    description: Optional[str]
    status: RegulatoryRiskStatus
    impact_level: ImpactLevel
    updated_at: datetime


class FintechComparableRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: Optional[uuid.UUID]
    comparable_name: str
    subvertical_id: Optional[uuid.UUID]
    geography: Optional[str]
    arr_usd: Optional[float]
    valuation_usd: Optional[float]
    arr_multiple: Optional[float]
    notes: Optional[str]


class FintechSubverticalSummary(BaseModel):
    subvertical: FintechSubverticalRead
    total_startups_in_portfolio: int
    avg_arr_usd: Optional[float]
    comparables_count: int
    unit_economics_count: int
    regulatory_risks_count: int


class FintechMarketOverview(BaseModel):
    total_subverticals: int
    subverticals: list[FintechSubverticalSummary]
    top_subvertical_by_investment: str
    latam_total_investment_usd: float
