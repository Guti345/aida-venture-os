import uuid
from datetime import date, datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    UUID, Date, DateTime, Enum, ForeignKey,
    Integer, String, Text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReportingFrequency(PyEnum):
    monthly = "monthly"
    quarterly = "quarterly"
    annual = "annual"


class LPTier(PyEnum):
    anchor = "anchor"
    core = "core"
    standard = "standard"


class ReportType(PyEnum):
    ic_memo = "ic_memo"
    lp_update = "lp_update"
    ppm = "ppm"
    sourcing_deck = "sourcing_deck"


class ReportStatus(PyEnum):
    draft = "draft"
    final = "final"
    archived = "archived"


class ICDecisionType(PyEnum):
    invest = "invest"
    pass_ = "pass"
    watchlist = "watchlist"


class LPProfile(Base):
    __tablename__ = "lp_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lp_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lps.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    preferred_metrics_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    reporting_frequency: Mapped[ReportingFrequency] = mapped_column(
        Enum(ReportingFrequency, name="reporting_frequency"), nullable=False
    )
    tier: Mapped[LPTier] = mapped_column(
        Enum(LPTier, name="lp_tier"), nullable=False
    )
    last_update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    lp: Mapped["LP"] = relationship(foreign_keys=[lp_id])


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    report_type: Mapped[ReportType] = mapped_column(
        Enum(ReportType, name="report_type"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    fund_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("funds.id", ondelete="RESTRICT"), nullable=False
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus, name="report_status"), nullable=False, default=ReportStatus.draft
    )
    content_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    fund: Mapped["Fund"] = relationship(foreign_keys=[fund_id])
    narrative_blocks: Mapped[list["NarrativeBlock"]] = relationship(back_populates="report")


class NarrativeBlock(Base):
    __tablename__ = "narrative_blocks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    section_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    data_references_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    report: Mapped["Report"] = relationship(back_populates="narrative_blocks")


class ICDecision(Base):
    __tablename__ = "ic_decisions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    deal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("deal_opportunities.id", ondelete="RESTRICT"), nullable=False, unique=True
    )
    decision: Mapped[ICDecisionType] = mapped_column(
        Enum(ICDecisionType, name="ic_decision_type"), nullable=False
    )
    decision_date: Mapped[date] = mapped_column(Date, nullable=False)
    committee_members_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_snapshot_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    deal: Mapped["DealOpportunity"] = relationship(foreign_keys=[deal_id])
