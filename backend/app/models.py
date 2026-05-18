"""
Pydantic models for the Real Estate & Property chatbot.
"""
from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel, Field


# ─── Request ───────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = None


# ─── Domain entities (loose dict-shapes used by handlers) ──
# We keep blocks dict-typed so handlers can resolve & enrich freely.


# ─── Rich message blocks ───────────────────────────────────
class TextBlock(BaseModel):
    type: Literal["text"] = "text"
    content: str


class DisclaimerBlock(BaseModel):
    type: Literal["disclaimer"] = "disclaimer"
    content: str


class FairHousingAlertBlock(BaseModel):
    """Shown when a user message triggers fair-housing or privacy/social-eng guards."""
    type: Literal["fair_housing_alert"] = "fair_housing_alert"
    headline: str
    message: str
    indicators: list[str]
    offer: str   # what we CAN do instead


class PropertyListBlock(BaseModel):
    type: Literal["property_list"] = "property_list"
    title: Optional[str] = None
    items: list[dict]
    total: int


class PropertyDetailBlock(BaseModel):
    type: Literal["property_detail"] = "property_detail"
    property: dict


class NeighborhoodBlock(BaseModel):
    type: Literal["neighborhood"] = "neighborhood"
    title: Optional[str] = None
    items: list[dict]


class ProjectBlock(BaseModel):
    type: Literal["project"] = "project"
    title: Optional[str] = None
    items: list[dict]


class EmiBlock(BaseModel):
    type: Literal["emi"] = "emi"
    property_price: int
    down_payment: int
    loan_amount: int
    interest_rate: float
    tenure_years: int
    emi: float
    total_interest: float
    total_payable: float


class AffordabilityBlock(BaseModel):
    type: Literal["affordability"] = "affordability"
    monthly_income: int
    obligations: int
    estimated_loan: int
    estimated_property_budget: int
    assumptions: list[str]


class ViewingBlock(BaseModel):
    type: Literal["viewing"] = "viewing"
    confirmation: dict


class ViewingListBlock(BaseModel):
    type: Literal["viewing_list"] = "viewing_list"
    items: list[dict]


class SavedSearchBlock(BaseModel):
    type: Literal["saved_search"] = "saved_search"
    items: list[dict]


class MarketTrendBlock(BaseModel):
    type: Literal["market_trend"] = "market_trend"
    title: str
    neighborhoods: list[dict]
    period: str


class CompareBlock(BaseModel):
    type: Literal["compare"] = "compare"
    properties: list[dict]
    attributes: list[str]


class DocumentChecklistBlock(BaseModel):
    type: Literal["document_checklist"] = "document_checklist"
    purpose: str
    items: list[dict]


MessageBlock = (
    TextBlock | DisclaimerBlock | FairHousingAlertBlock
    | PropertyListBlock | PropertyDetailBlock | NeighborhoodBlock | ProjectBlock
    | EmiBlock | AffordabilityBlock | ViewingBlock | ViewingListBlock
    | SavedSearchBlock | MarketTrendBlock | CompareBlock | DocumentChecklistBlock
)


# ─── Response ──────────────────────────────────────────────
class ChatResponse(BaseModel):
    session_id: str
    intent: str
    confidence: float
    blocks: list[MessageBlock]
    suggestions: list[str] = []
    safety_flag: Optional[str] = None   # None | "fair_housing" | "privacy" | "social_engineering"
