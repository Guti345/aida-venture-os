import uuid
from datetime import date, datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    UUID, Date, DateTime, Enum, ForeignKey,
    Integer, Numeric, String, Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MarketStage(PyEnum):
    pre_seed = "pre_seed"
    seed = "seed"
    series_a = "series_a"
    series_b = "series_b"


class MultipleType(PyEnum):
    ARR = "ARR"
    EV_Revenue = "EV_Revenue"
    EBITDA = "EBITDA"
    GMV = "GMV"


class MarketSegment(Base):
    __tablename__ = "market_segments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    subsector: Mapped[str | None] = mapped_column(String(100), nullable=True)
    stage: Mapped[MarketStage] = mapped_column(
        Enum(MarketStage, name="market_stage"), nullable=False
    )
    geography: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    benchmark_entries: Mapped[list["BenchmarkEntry"]] = relationship(back_populates="segment")
    benchmark_series: Mapped[list["BenchmarkSeries"]] = relationship(back_populates="segment")
    valuation_distributions: Mapped[list["ValuationDistribution"]] = relationship(back_populates="segment")


class BenchmarkEntry(Base):
    __tablename__ = "benchmark_entries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    segment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("market_segments.id", ondelete="CASCADE"), nullable=False
    )
    multiple_type: Mapped[MultipleType] = mapped_column(
        Enum(MultipleType, name="multiple_type"), nullable=False
    )
    p10: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    p25: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    p50: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    p75: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    p90: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    reference_date: Mapped[date] = mapped_column(Date, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    segment: Mapped["MarketSegment"] = relationship(back_populates="benchmark_entries")


class BenchmarkSeries(Base):
    __tablename__ = "benchmark_series"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    segment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("market_segments.id", ondelete="CASCADE"), nullable=False
    )
    multiple_type: Mapped[str] = mapped_column(String(100), nullable=False)
    period_date: Mapped[date] = mapped_column(Date, nullable=False)
    median_value: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)

    segment: Mapped["MarketSegment"] = relationship(back_populates="benchmark_series")


class ValuationDistribution(Base):
    __tablename__ = "valuation_distributions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    segment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("market_segments.id", ondelete="CASCADE"), nullable=False
    )
    reference_date: Mapped[date] = mapped_column(Date, nullable=False)
    p10: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    p25: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    p50: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    p75: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    p90: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    sample_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)

    segment: Mapped["MarketSegment"] = relationship(back_populates="valuation_distributions")
