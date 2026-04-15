import uuid
from datetime import date, datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    UUID, Date, DateTime, Enum, ForeignKey,
    Numeric, String, Text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RiskLevel(PyEnum):
    low = "low"
    medium = "medium"
    high = "high"


class RegulatoryComplexity(PyEnum):
    low = "low"
    medium = "medium"
    high = "high"


class RegulatoryRiskStatus(PyEnum):
    active = "active"
    mitigated = "mitigated"
    pending = "pending"


class ImpactLevel(PyEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class FintechSubvertical(Base):
    __tablename__ = "fintech_subverticals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level"), nullable=False
    )
    regulatory_complexity: Mapped[RegulatoryComplexity] = mapped_column(
        Enum(RegulatoryComplexity, name="regulatory_complexity"), nullable=False
    )
    key_metrics_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    unit_economics: Mapped[list["FintechUnitEconomics"]] = relationship(back_populates="subvertical")
    comparables: Mapped[list["FintechComparable"]] = relationship(back_populates="subvertical")


class FintechUnitEconomics(Base):
    __tablename__ = "fintech_unit_economics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="CASCADE"), nullable=False
    )
    subvertical_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("fintech_subverticals.id", ondelete="SET NULL"), nullable=True
    )
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(24, 6), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    period_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    startup: Mapped["Startup"] = relationship(foreign_keys=[startup_id])
    subvertical: Mapped["FintechSubvertical"] = relationship(back_populates="unit_economics")


class RegulatoryRisk(Base):
    __tablename__ = "regulatory_risks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="CASCADE"), nullable=False
    )
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    risk_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[RegulatoryRiskStatus] = mapped_column(
        Enum(RegulatoryRiskStatus, name="regulatory_risk_status"), nullable=False
    )
    impact_level: Mapped[ImpactLevel] = mapped_column(
        Enum(ImpactLevel, name="impact_level"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    startup: Mapped["Startup"] = relationship(foreign_keys=[startup_id])


class FintechComparable(Base):
    __tablename__ = "fintech_comparables"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="SET NULL"), nullable=True
    )
    comparable_name: Mapped[str] = mapped_column(String(255), nullable=False)
    subvertical_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("fintech_subverticals.id", ondelete="SET NULL"), nullable=True
    )
    geography: Mapped[str | None] = mapped_column(String(100), nullable=True)
    arr_usd: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    valuation_usd: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    arr_multiple: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    startup: Mapped["Startup"] = relationship(foreign_keys=[startup_id])
    subvertical: Mapped["FintechSubvertical"] = relationship(back_populates="comparables")
