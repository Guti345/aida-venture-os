import uuid
from datetime import date, datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    UUID, Boolean, Date, DateTime, Enum, ForeignKey,
    Integer, Numeric, String, Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SourcingChannelType(PyEnum):
    network = "network"
    accelerator = "accelerator"
    inbound = "inbound"
    studio = "studio"
    event = "event"
    cold = "cold"


class DealStatus(PyEnum):
    identified = "identified"
    screening = "screening"
    dd = "dd"
    ic = "ic"
    invested = "invested"
    passed = "passed"
    watchlist = "watchlist"


class DDItemCategory(PyEnum):
    team = "team"
    product = "product"
    market = "market"
    financials = "financials"
    legal = "legal"
    tech = "tech"


class DDItemStatus(PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"
    na = "na"


class ICRecommendation(PyEnum):
    invest = "invest"
    pass_ = "pass"
    watchlist = "watchlist"


class SourcingChannel(Base):
    __tablename__ = "sourcing_channels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[SourcingChannelType] = mapped_column(
        Enum(SourcingChannelType, name="sourcing_channel_type"), nullable=False
    )
    contact_person: Mapped[str | None] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    deals: Mapped[list["DealOpportunity"]] = relationship(back_populates="sourcing_channel")


class DealOpportunity(Base):
    __tablename__ = "deal_opportunities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    startup_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("startups.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[DealStatus] = mapped_column(
        Enum(DealStatus, name="deal_status"), nullable=False
    )
    sourcing_channel_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sourcing_channels.id", ondelete="SET NULL"), nullable=True
    )
    introduced_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    identified_at: Mapped[date] = mapped_column(Date, nullable=False)
    screening_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    dd_start_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    ic_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    decision: Mapped[str | None] = mapped_column(String(255), nullable=True)
    decision_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    startup: Mapped["Startup"] = relationship(foreign_keys=[startup_id])
    sourcing_channel: Mapped["SourcingChannel"] = relationship(back_populates="deals")
    thesis_alignments: Mapped[list["ThesisAlignment"]] = relationship(back_populates="deal")
    dd_checklists: Mapped[list["DDChecklist"]] = relationship(back_populates="deal")
    ic_memos: Mapped[list["ICMemo"]] = relationship(back_populates="deal")


class ThesisAlignment(Base):
    __tablename__ = "thesis_alignments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    deal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("deal_opportunities.id", ondelete="CASCADE"), nullable=False
    )
    thesis_dimension: Mapped[str] = mapped_column(String(255), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    deal: Mapped["DealOpportunity"] = relationship(back_populates="thesis_alignments")


class DDChecklist(Base):
    __tablename__ = "dd_checklists"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    deal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("deal_opportunities.id", ondelete="CASCADE"), nullable=False
    )
    item_category: Mapped[DDItemCategory] = mapped_column(
        Enum(DDItemCategory, name="dd_item_category"), nullable=False
    )
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[DDItemStatus] = mapped_column(
        Enum(DDItemStatus, name="dd_item_status"), nullable=False, default=DDItemStatus.pending
    )
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    deal: Mapped["DealOpportunity"] = relationship(back_populates="dd_checklists")


class ICMemo(Base):
    __tablename__ = "ic_memos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    deal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("deal_opportunities.id", ondelete="CASCADE"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    recommendation: Mapped[ICRecommendation] = mapped_column(
        Enum(ICRecommendation, name="ic_recommendation"), nullable=False
    )
    valuation_proposed: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    key_risks: Mapped[str | None] = mapped_column(Text, nullable=True)
    key_upside: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    deal: Mapped["DealOpportunity"] = relationship(back_populates="ic_memos")
