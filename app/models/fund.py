import uuid
from datetime import date, datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    UUID, Date, DateTime, Enum, ForeignKey,
    Integer, Numeric, String
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class FundStatus(PyEnum):
    fundraising = "fundraising"
    investing = "investing"
    harvesting = "harvesting"
    closed = "closed"


class LPType(PyEnum):
    individual = "individual"
    institutional = "institutional"
    family_office = "family_office"
    fund_of_funds = "fund_of_funds"


class InvestmentType(PyEnum):
    lead = "lead"
    co_invest = "co_invest"
    follow_on = "follow_on"


class ScenarioType(PyEnum):
    base = "base"
    high = "high"
    downside = "downside"


class Fund(Base):
    __tablename__ = "funds"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    vintage_year: Mapped[int] = mapped_column(Integer, nullable=False)
    target_size_usd: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    deployed_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    geography_focus: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stage_focus: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[FundStatus] = mapped_column(
        Enum(FundStatus, name="fund_status"), nullable=False
    )

    lps: Mapped[list["LP"]] = relationship(back_populates="fund")
    investments: Mapped[list["Investment"]] = relationship(back_populates="fund")
    scenarios: Mapped[list["FundScenario"]] = relationship(back_populates="fund")
    metrics: Mapped[list["FundMetric"]] = relationship(back_populates="fund")


class LP(Base):
    __tablename__ = "lps"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fund_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("funds.id", ondelete="RESTRICT"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[LPType] = mapped_column(
        Enum(LPType, name="lp_type"), nullable=False
    )
    committed_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    called_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    distributed_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    joined_at: Mapped[date] = mapped_column(Date, nullable=False)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    fund: Mapped["Fund"] = relationship(back_populates="lps")


class Investment(Base):
    __tablename__ = "investments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="RESTRICT"), nullable=False
    )
    fund_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("funds.id", ondelete="RESTRICT"), nullable=False
    )
    round_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("funding_rounds.id", ondelete="SET NULL"), nullable=True
    )
    amount_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    pre_money_val: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    equity_pct: Mapped[float] = mapped_column(Numeric(7, 4), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    investment_type: Mapped[InvestmentType] = mapped_column(
        Enum(InvestmentType, name="investment_type"), nullable=False
    )
    follow_on_reserve_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)

    startup: Mapped["Startup"] = relationship(foreign_keys=[startup_id])
    fund: Mapped["Fund"] = relationship(back_populates="investments")
    round: Mapped["FundingRound"] = relationship(foreign_keys=[round_id])


class FundScenario(Base):
    __tablename__ = "fund_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fund_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("funds.id", ondelete="CASCADE"), nullable=False
    )
    scenario_type: Mapped[ScenarioType] = mapped_column(
        Enum(ScenarioType, name="scenario_type"), nullable=False
    )
    moic_p25: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    moic_p50: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    moic_p75: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    irr_p25: Mapped[float] = mapped_column(Numeric(8, 6), nullable=False)
    irr_p50: Mapped[float] = mapped_column(Numeric(8, 6), nullable=False)
    irr_p75: Mapped[float] = mapped_column(Numeric(8, 6), nullable=False)
    dpi_projected: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    tvpi_projected: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    run_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    assumptions_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    fund: Mapped["Fund"] = relationship(back_populates="scenarios")


class FundMetric(Base):
    __tablename__ = "fund_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fund_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("funds.id", ondelete="CASCADE"), nullable=False
    )
    calculation_date: Mapped[date] = mapped_column(Date, nullable=False)
    moic: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    tvpi: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    dpi: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    rvpi: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    irr: Mapped[float | None] = mapped_column(Numeric(8, 6), nullable=True)
    total_invested_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    total_fmv_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    total_realized_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)

    fund: Mapped["Fund"] = relationship(back_populates="metrics")
