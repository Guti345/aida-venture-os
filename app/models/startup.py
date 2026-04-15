import uuid
from datetime import date, datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    UUID, Boolean, Date, DateTime, Enum, ForeignKey,
    Numeric, String, Text, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StartupStage(PyEnum):
    pre_seed = "pre_seed"
    seed = "seed"
    series_a = "series_a"
    series_b = "series_b"
    bridge = "bridge"


class StartupStatus(PyEnum):
    active = "active"
    exited = "exited"
    dead = "dead"
    watchlist = "watchlist"


class RoundType(PyEnum):
    pre_seed = "pre_seed"
    seed = "seed"
    series_a = "series_a"
    series_b = "series_b"
    bridge = "bridge"


class RoundStatus(PyEnum):
    closed = "closed"
    announced = "announced"
    rumored = "rumored"


class PeriodType(PyEnum):
    monthly = "monthly"
    quarterly = "quarterly"
    annual = "annual"


class Startup(Base):
    __tablename__ = "startups"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    subsector: Mapped[str | None] = mapped_column(String(100), nullable=True)
    stage: Mapped[StartupStage] = mapped_column(
        Enum(StartupStage, name="startup_stage"), nullable=False
    )
    geography: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(2), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    founded_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    studio_built: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[StartupStatus] = mapped_column(
        Enum(StartupStatus, name="startup_status"), nullable=False, default=StartupStatus.active
    )
    is_simulated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    founders: Mapped[list["StartupFounder"]] = relationship(back_populates="startup")
    funding_rounds: Mapped[list["FundingRound"]] = relationship(back_populates="startup")
    metric_snapshots: Mapped[list["MetricSnapshot"]] = relationship(back_populates="startup")


class Founder(Base):
    __tablename__ = "founders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    background: Mapped[str | None] = mapped_column(Text, nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    startups: Mapped[list["StartupFounder"]] = relationship(back_populates="founder")


class StartupFounder(Base):
    __tablename__ = "startup_founders"
    __table_args__ = (
        UniqueConstraint("startup_id", "founder_id", name="uq_startup_founder"),
    )

    startup_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="CASCADE"), primary_key=True
    )
    founder_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("founders.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    equity_pct: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    startup: Mapped["Startup"] = relationship(back_populates="founders")
    founder: Mapped["Founder"] = relationship(back_populates="startups")


class FundingRound(Base):
    __tablename__ = "funding_rounds"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="CASCADE"), nullable=False
    )
    round_type: Mapped[RoundType] = mapped_column(
        Enum(RoundType, name="round_type"), nullable=False
    )
    amount_usd: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    pre_money_val: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    post_money_val: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    lead_investor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[RoundStatus] = mapped_column(
        Enum(RoundStatus, name="round_status"), nullable=False, default=RoundStatus.closed
    )

    startup: Mapped["Startup"] = relationship(back_populates="funding_rounds")


class MetricSnapshot(Base):
    __tablename__ = "metric_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="CASCADE"), nullable=False
    )
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(24, 6), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    period_date: Mapped[date] = mapped_column(Date, nullable=False)
    period_type: Mapped[PeriodType] = mapped_column(
        Enum(PeriodType, name="period_type"), nullable=False
    )
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    startup: Mapped["Startup"] = relationship(back_populates="metric_snapshots")
