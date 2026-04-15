import uuid
from datetime import date, datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    UUID, Boolean, Date, DateTime, Enum, ForeignKey,
    Numeric, String, Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ValuationVerdict(PyEnum):
    within_range = "within_range"
    premium_justified = "premium_justified"
    overvalued = "overvalued"
    undervalued = "undervalued"


class DriverType(PyEnum):
    nrr = "nrr"
    rule_of_40 = "rule_of_40"
    growth_rate = "growth_rate"
    ltv_cac = "ltv_cac"
    gross_margin = "gross_margin"


class FlagType(PyEnum):
    overvalued = "overvalued"
    undervalued = "undervalued"
    top_performer = "top_performer"
    underperformer = "underperformer"


class ValuationEvent(Base):
    __tablename__ = "valuation_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="CASCADE"), nullable=False
    )
    round_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("funding_rounds.id", ondelete="SET NULL"), nullable=True
    )
    pre_money_val: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    arr_at_time: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    multiple_paid: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    segment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("market_segments.id", ondelete="SET NULL"), nullable=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)

    startup: Mapped["Startup"] = relationship(foreign_keys=[startup_id])
    round: Mapped["FundingRound"] = relationship(foreign_keys=[round_id])
    segment: Mapped["MarketSegment"] = relationship(foreign_keys=[segment_id])
    multiple_analyses: Mapped[list["MultipleAnalysis"]] = relationship(back_populates="valuation_event")


class MultipleAnalysis(Base):
    __tablename__ = "multiple_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    valuation_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("valuation_events.id", ondelete="CASCADE"), nullable=False
    )
    segment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("market_segments.id", ondelete="RESTRICT"), nullable=False
    )
    multiple_paid: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    market_p25: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    market_p50: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    market_p75: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    premium_pct: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    verdict: Mapped[ValuationVerdict] = mapped_column(
        Enum(ValuationVerdict, name="valuation_verdict"), nullable=False
    )
    justification: Mapped[str | None] = mapped_column(Text, nullable=True)

    valuation_event: Mapped["ValuationEvent"] = relationship(back_populates="multiple_analyses")
    segment: Mapped["MarketSegment"] = relationship(foreign_keys=[segment_id])


class ValuationDriver(Base):
    __tablename__ = "valuation_drivers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="CASCADE"), nullable=False
    )
    driver_type: Mapped[DriverType] = mapped_column(
        Enum(DriverType, name="driver_type"), nullable=False
    )
    value: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    benchmark_threshold: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    above_threshold: Mapped[bool] = mapped_column(Boolean, nullable=False)
    premium_justified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    startup: Mapped["Startup"] = relationship(foreign_keys=[startup_id])


class OutlierFlag(Base):
    __tablename__ = "outlier_flags"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="CASCADE"), nullable=False
    )
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(24, 6), nullable=False)
    market_p25: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    market_p75: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    flag_type: Mapped[FlagType] = mapped_column(
        Enum(FlagType, name="flag_type"), nullable=False
    )
    flagged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    startup: Mapped["Startup"] = relationship(foreign_keys=[startup_id])
