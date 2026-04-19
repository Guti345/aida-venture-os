import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.dealflow import (
    DDItemCategory, DDItemStatus, DealStatus,
    ICRecommendation, SourcingChannelType,
)


class SourcingChannelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    type: SourcingChannelType
    contact_person: Optional[str]
    active: bool
    notes: Optional[str]


class DealOpportunityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: Optional[uuid.UUID]
    status: DealStatus
    sourcing_channel_id: Optional[uuid.UUID]
    introduced_by: Optional[str]
    identified_at: date
    screening_at: Optional[date]
    dd_start_at: Optional[date]
    ic_date: Optional[date]
    decision: Optional[str]
    decision_notes: Optional[str]


class DealOpportunityWithStartup(DealOpportunityRead):
    startup_name: Optional[str] = None
    sourcing_channel_name: Optional[str] = None


class ThesisAlignmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    deal_id: uuid.UUID
    thesis_dimension: str
    score: int
    max_score: int
    notes: Optional[str]


class DDChecklistRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    deal_id: uuid.UUID
    item_category: DDItemCategory
    item_name: str
    status: DDItemStatus
    due_date: Optional[date]
    notes: Optional[str]


class ICMemoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    deal_id: uuid.UUID
    version: int
    recommendation: ICRecommendation
    valuation_proposed: Optional[float]
    key_risks: Optional[str]
    key_upside: Optional[str]
    created_at: datetime


class DealSummary(BaseModel):
    total_deals: int
    deals_by_status: dict[str, int]
    avg_thesis_score: Optional[float]
    deals_this_month: int


class DealDetailRead(BaseModel):
    deal: DealOpportunityWithStartup
    thesis_alignments: list[ThesisAlignmentRead]
    dd_checklist: list[DDChecklistRead]
    ic_memos: list[ICMemoRead]
