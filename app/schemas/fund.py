import uuid
from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.fund import FundStatus, InvestmentType, ScenarioType


class FundRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    vintage_year: int
    target_size_usd: Optional[float]
    deployed_usd: float
    currency: str
    geography_focus: Optional[str]
    stage_focus: Optional[str]
    status: FundStatus


class InvestmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    startup_name: Optional[str] = None
    fund_id: uuid.UUID
    round_id: Optional[uuid.UUID]
    amount_usd: float
    pre_money_val: Optional[float]
    equity_pct: float
    date: date
    investment_type: InvestmentType
    follow_on_reserve_usd: float

    @classmethod
    def from_orm_with_name(cls, inv) -> "InvestmentRead":
        obj = cls.model_validate(inv)
        if inv.startup is not None:
            obj.startup_name = inv.startup.name
        return obj


class FundMetricsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    fund_id: uuid.UUID
    calculation_date: date
    moic: float
    tvpi: float
    dpi: float
    rvpi: float
    irr: Optional[float]
    total_invested_usd: float
    total_fmv_usd: float
    total_realized_usd: float


class FundScenarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    fund_id: uuid.UUID
    scenario_type: ScenarioType
    moic_p25: float
    moic_p50: float
    moic_p75: float
    irr_p25: float
    irr_p50: float
    irr_p75: float
    dpi_projected: float
    tvpi_projected: float
    run_date: datetime
    assumptions_json: Optional[dict]


class ScenarioInput(BaseModel):
    fund_id: uuid.UUID
    n_iterations: int = Field(default=1000, ge=100, le=10_000)
    pct_winners: float = Field(default=0.20, ge=0.0, le=1.0)
    avg_winner_multiple: float = Field(default=15.0, ge=1.0)
    avg_loss_rate: float = Field(default=0.40, ge=0.0, le=1.0)
    fund_life_years: int = Field(default=10, ge=1, le=30)
    mgmt_fee_pct: float = Field(default=2.0, ge=0.0, le=5.0)
    carry_pct: float = Field(default=20.0, ge=0.0, le=40.0)


class ScenarioResult(BaseModel):
    scenario_type: ScenarioType
    moic_p25: float
    moic_p50: float
    moic_p75: float
    irr_p25: float
    irr_p50: float
    irr_p75: float
    dpi_projected: float
    tvpi_projected: float
    total_invested_usd: float
    n_iterations: int
    assumptions: dict[str, Any]
