import uuid
from datetime import date, datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    UUID, Boolean, Date, DateTime, Enum, ForeignKey,
    Numeric, String, Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StudioSupportLevel(PyEnum):
    full = "full"
    partial = "partial"
    accelerator = "accelerator"


class StudioPhase(PyEnum):
    idea = "idea"
    validation = "validation"
    mvp = "mvp"
    first_revenue = "first_revenue"
    pmf = "pmf"
    seed = "seed"
    series_a_prep = "series_a_prep"


class BuildCostType(PyEnum):
    personnel = "personnel"
    tech = "tech"
    ops = "ops"
    legal = "legal"
    marketing = "marketing"
    capex = "capex"


class MilestoneType(PyEnum):
    idea = "idea"
    validation = "validation"
    mvp = "mvp"
    first_revenue = "first_revenue"
    pmf = "pmf"
    seed = "seed"
    series_a = "series_a"


class StudioCompany(Base):
    __tablename__ = "studio_companies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="RESTRICT"), nullable=False, unique=True
    )
    idea_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    validation_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    mvp_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    pmf_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    first_external_seed_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    build_cost_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    equity_retained_pct: Mapped[float | None] = mapped_column(Numeric(7, 4), nullable=True)
    studio_support_level: Mapped[StudioSupportLevel] = mapped_column(
        Enum(StudioSupportLevel, name="studio_support_level"), nullable=False
    )
    current_studio_phase: Mapped[StudioPhase] = mapped_column(
        Enum(StudioPhase, name="studio_phase"), nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    startup: Mapped["Startup"] = relationship(foreign_keys=[startup_id])
    build_costs: Mapped[list["BuildCost"]] = relationship(back_populates="studio_company")
    milestones: Mapped[list["StudioMilestone"]] = relationship(back_populates="studio_company")
    alpha_metrics: Mapped[list["AlphaMetric"]] = relationship(back_populates="studio_company")


class BuildCost(Base):
    __tablename__ = "build_costs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    studio_company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("studio_companies.id", ondelete="CASCADE"), nullable=False
    )
    cost_type: Mapped[BuildCostType] = mapped_column(
        Enum(BuildCostType, name="build_cost_type"), nullable=False
    )
    amount_usd: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    period_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    studio_company: Mapped["StudioCompany"] = relationship(back_populates="build_costs")


class StudioMilestone(Base):
    __tablename__ = "studio_milestones"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    studio_company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("studio_companies.id", ondelete="CASCADE"), nullable=False
    )
    milestone_type: Mapped[MilestoneType] = mapped_column(
        Enum(MilestoneType, name="milestone_type"), nullable=False
    )
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    actual_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    achieved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    studio_company: Mapped["StudioCompany"] = relationship(back_populates="milestones")


class AlphaMetric(Base):
    __tablename__ = "alpha_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    studio_company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("studio_companies.id", ondelete="CASCADE"), nullable=False
    )
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    studio_value: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    market_benchmark: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    delta_pct: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    is_alpha: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    studio_company: Mapped["StudioCompany"] = relationship(back_populates="alpha_metrics")
