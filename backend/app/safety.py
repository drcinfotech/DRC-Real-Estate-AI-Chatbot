"""
Fair-housing safety layer for the Real Estate chatbot.

This is the gravest harm category in real estate AI: facilitating housing
discrimination. Both the US Fair Housing Act (42 USC §3604) and India's
Article 15 of the Constitution / various state housing laws prohibit
discrimination based on protected characteristics. Online real-estate
platforms have repeatedly been found liable for allowing search filters
that proxy for these characteristics.

This module catches:
  • Direct discrimination: "only for X religion / caste / community"
  • Coded proxies: "safe neighborhoods" (race proxy), "good schools"
    (also race proxy in some contexts), "no kids", "family only"
  • Privacy: trying to look up owner identity or contact details for
    properties the user isn't a verified lead on
  • Social engineering: prompt injection

Conservative by design — when in doubt, refuse and explain why.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class SafetyResult:
    flag: Optional[Literal["fair_housing", "privacy", "social_engineering"]]
    reason: str = ""


# ─── Direct fair-housing violations ───────────────────────
# Explicit filtering by a protected characteristic.
FAIR_HOUSING_PATTERNS = [
    # Religion / caste / community filtering
    r"\b(only|just|prefer(?:ably)?|want|need|looking for|find me)\b.{0,40}\b(hindu|muslim|christian|jain|sikh|parsi|buddhist|jewish|catholic|protestant)\b.{0,30}\b(area|locality|neighborhood|colony|society|tenant|landlord|owner|building|community)",
    r"\b(no|not?)\b.{0,15}\b(hindu|muslim|christian|jain|sikh|parsi|buddhist|jewish|catholic|protestant|non-?vegetarian|non-?veg)\b.{0,30}\b(area|locality|neighborhood|tenant|landlord|owner|building|community)",
    r"\b(hindu|muslim|christian|jain|sikh|parsi)\s+only\b",
    r"\b(brahmin|kshatriya|vaishya|patel|gujarati|marwari|tamil|punjabi|bengali)\s+(only|preferred|tenants?|community|building|society)\b",
    r"\b(caste|religion)[\s-]?(based|specific|preferred|filter)",
    r"\bsame\s+(caste|religion|community|background)\b.{0,20}(tenant|owner|society)",

    # Race / nationality / ethnicity filtering
    r"\b(white|black|asian|african|chinese|indian|foreign(?:ers?)?)\b.{0,30}\b(only|preferred|not allowed|no)\b.{0,20}\b(tenant|building|society|area|neighborhood)",
    r"\b(no|not allowed)\s+(foreigners?|immigrants?|outsiders?|north\s+indians?|south\s+indians?|bihari|nepali|bangladeshi)\b",
    r"\b(only|just)\s+(locals?|natives?|gujaratis?|marwaris?|punjabis?)\s+(tenants?|preferred|allowed)",

    # Family status / marital status discrimination
    r"\b(no|not?\s+want(?:ing)?|don'?t want|avoid)\s+(kids?|children|families|family|couples?|married|babies)\b",
    r"\b(bachelors?|single|unmarried)\s+only\b",
    r"\bno\s+(bachelors?|single\s+(men|women|guys|girls))\b",
    r"\bfamily\s+only\b.{0,30}\b(building|society|tenant|preferred)",
    r"\b(no|not for)\s+(pregnant|expecting|maternity)",

    # Disability / age discrimination
    r"\bno\s+(disabled|handicapped|wheel-?chair|elderly|old|senior)\s+(tenants?|residents?|people)",
    r"\b(young|youth)\s+only\b.{0,20}\b(tenant|society|building)",
    r"\bable[-\s]?bodied\s+only\b",

    # Gender discrimination
    r"\bno\s+(women|girls|females?|men|males?|boys)\s+(tenants?|allowed)",
    r"\b(women|girls|men|boys)\s+only\b.{0,15}\b(building|society|floor)",

    # Coded proxies — these are the trickiest. Phrases that frequently
    # function as discriminatory filters even when superficially neutral.
    r"\b(safe|good)\s+neighborhood\s+for\s+(my\s+)?(white|black|hindu|muslim|jewish|christian|asian|indian|foreign)",
    r"\bareas?\s+with\s+(low|less|fewer|no)\s+(muslims?|hindus?|christians?|foreigners?|immigrants?|migrants?)",
    r"\bavoid\s+(muslim|hindu|christian|migrant|immigrant|foreigner|bachelor|low.?income|slum)\s+(areas?|localities|neighborhoods?|colonies)",

    # Help me write a discriminatory listing
    r"\b(write|draft|create|help me make)\b.{0,30}\b(listing|ad|advert(?:isement)?|post)\b.{0,40}\b(no\s+\w+|only\s+\w+|prefer\s+\w+)\b.{0,20}(community|religion|caste|tenants?|bachelors?|kids?|family|families)",
]


# ─── Privacy patterns (owner data, other users' searches) ──
PRIVACY_PATTERNS = [
    # Asking for the owner / seller's personal contact when not a verified lead
    r"\b(owner'?s?|seller'?s?|landlord'?s?)\s+(personal\s+)?(phone|mobile|number|email|address|home address|whatsapp|name)",
    r"\b(give|tell|share|reveal|show)\s+me\s+(the\s+)?(owner'?s?|seller'?s?|landlord'?s?)\s+(phone|number|details|info|contact)",
    r"\bwho\s+(is|owns)\s+(the\s+)?(seller|owner|landlord)\s+(of|for)",
    r"\b(owner'?s?|seller'?s?)\s+(direct\s+)?(contact|details|number|phone)\b.{0,30}\b(without|skip(?:ping)?|bypass(?:ing)?|going\s+around)\s+(the\s+|an?\s+)?(agent|broker)",
    r"\bbypass(?:ing)?\s+(the\s+)?(agent|broker)\s+(and\s+)?(get|find|contact)\s+(the\s+)?(owner|seller|landlord)",

    # Snooping into another user's data
    r"\b(show|view|list)\s+(another|other)\s+users?'?s?\s+(searches|saved|viewings|leads)",
]


# ─── Social engineering / prompt injection ─────────────────
SOCIAL_ENGINEERING_PATTERNS = [
    r"\b(ignore|disregard|forget)\s+(\w+\s+){0,4}(instructions|rules|guidelines|system\s+prompt|safety)",
    r"\byou\s+are\s+now\s+(in\s+|an?\s+)?(admin|administrator|dev|developer|debug|root|owner|landlord)\s+(mode|user)?",
    r"\bpretend\s+(you\s+are|to\s+be)\s+(an?\s+)?(admin|root|developer|owner|landlord|agent\s+with\s+full\s+access)",
    r"\b(give|provide|reveal|show|tell)\s+(me\s+)?(your\s+)?(system\s+prompt|instructions|api\s+key|source\s+code)",
    r"\benable\s+(developer|admin|debug|root)\s+mode\b",
    r"\bjailbreak\b",
    r"\bDAN\s+mode\b",
    r"\bact\s+as\s+(if\s+)?(you\s+have\s+)?no\s+(rules|restrictions|guidelines|fair.?housing)",
]


def check_safety(text: str) -> SafetyResult:
    t = text.lower()

    for pat in SOCIAL_ENGINEERING_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="social_engineering", reason=pat)

    for pat in FAIR_HOUSING_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="fair_housing", reason=pat)

    for pat in PRIVACY_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="privacy", reason=pat)

    return SafetyResult(flag=None)


def build_fair_housing_block() -> dict:
    return {
        "type": "fair_housing_alert",
        "headline": "I can't filter homes by who lives there.",
        "message": (
            "I noticed your search seems to filter properties or neighborhoods by protected characteristics — "
            "things like religion, caste, community, race, family status, or disability. Doing so would violate "
            "fair-housing principles (Article 15 of the Indian Constitution, the US Fair Housing Act, and "
            "equivalent laws in most jurisdictions). I won't help with that."
        ),
        "indicators": [
            "Online platforms have been held liable for offering discriminatory search filters",
            "Coded phrases ('only families', 'preferred community', 'bachelors not allowed') count too",
            "These rules protect both renters/buyers AND owners — they cut both ways",
        ],
        "offer": (
            "What I CAN do: search by neutral criteria like budget, BHK, neighborhood, carpet area, amenities, "
            "RERA registration, proximity to schools or transit, or commute time. Want to try that instead?"
        ),
    }


def build_privacy_block() -> dict:
    return {
        "type": "fair_housing_alert",
        "headline": "I can't share owner contact details directly.",
        "message": (
            "Owner and seller contact information is protected. In this demo, contact is brokered through "
            "the listing agent until a viewing is confirmed — that protects everyone from spam, scams, "
            "and unauthorized commercial use of personal data."
        ),
        "indicators": [
            "India's DPDP Act 2023 and similar laws restrict sharing personal contact data without consent",
            "Most platforms route contact through agents until a verified lead is established",
            "Listed agents can put you in direct touch with the owner once a viewing is set",
        ],
        "offer": "I can schedule a viewing, send a message to the listing agent, or pull up the property details. Want to do any of those?",
    }


def build_social_engineering_block() -> dict:
    return {
        "type": "fair_housing_alert",
        "headline": "I can't do that.",
        "message": (
            "I'm not able to bypass my safety rules, switch into an 'admin' or 'agent' mode with elevated "
            "permissions, or reveal internal instructions. If you have a genuine real-estate question, "
            "I'm happy to help with that instead."
        ),
        "indicators": [
            "I work the same way for everyone — there's no privileged mode to unlock",
            "Real listing agents and brokers can do things I can't (close deals, share owner details, etc.)",
            "Use 'Talk to an agent' if you need something beyond search and viewing tools",
        ],
        "offer": "Try asking about properties, neighborhoods, EMI estimates, or scheduling a viewing.",
    }
