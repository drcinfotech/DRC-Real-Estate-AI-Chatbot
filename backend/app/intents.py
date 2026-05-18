"""
Intent classifier for the Real Estate & Property chatbot.

Safety detection (see safety.py) runs BEFORE this classifier.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IntentSpec:
    name: str
    patterns: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)


INTENTS: list[IntentSpec] = [
    IntentSpec(
        "greeting",
        patterns=[r"^\s*(hi|hello|hey|hola|namaste|good (morning|afternoon|evening))\b"],
        keywords=["hi", "hello", "hey", "hola", "namaste"],
    ),
    IntentSpec(
        "goodbye",
        patterns=[r"\b(bye|goodbye|see ya|see you|cya|take care)\b"],
        keywords=["bye", "goodbye"],
    ),
    IntentSpec(
        "thanks",
        patterns=[r"^\s*(thanks|thank you|thx|ty|appreciate it)\b"],
        keywords=["thanks", "thank"],
    ),
    IntentSpec(
        "search_buy",
        patterns=[
            r"\b(find|search|show|looking for|want)\b.{0,30}\b(buy|purchase|sale|own)\b",
            r"\b(properties?|flats?|apartments?|villas?|houses?|homes?)\s+(for\s+)?(sale|sell|buy|purchase)",
            r"\bbuy\s+(a|an?)?\s*\d?\s*(bhk|bedroom|flat|apartment|villa|house|home|property)",
            r"\b(for\s+)?sale\s+in\s+\w+",
        ],
        keywords=["buy", "for sale", "purchase"],
    ),
    IntentSpec(
        "search_rent",
        patterns=[
            r"\b(find|search|show|looking for|want|need)\b.{0,30}\b(rent|rentals?|lease|let)\b",
            r"\b(properties?|flats?|apartments?|villas?|houses?|homes?)\s+(for\s+)?rent",
            r"\brent\s+(a|an?)?\s*\d?\s*(bhk|bedroom|flat|apartment|villa|house|home|property)",
            r"\b(for\s+)?rent\s+in\s+\w+",
            r"\brental\s+(in|near|around)",
            r"\bbhk\s+rentals?\b",
        ],
        keywords=["rent", "rental", "rentals", "lease", "for rent"],
    ),
    IntentSpec(
        "search_commercial",
        patterns=[
            r"\b(commercial|office|shop|showroom|retail|warehouse|godown)\s+(space|property|for\s+rent|for\s+sale)",
            r"\bcommercial\s+(real\s+estate|property|listing)",
            r"\boffice\s+(space|in|near|around)",
            r"\bshowroom\s+(in|near|on)",
        ],
        keywords=["commercial", "office space", "showroom", "retail"],
    ),
    IntentSpec(
        "property_detail",
        patterns=[
            r"\b(show|view|see|tell me about|details? of)\s+(more about\s+)?(property|listing|prop-?\d+)",
            r"\bprop-?\d+\b",
            r"\bmore (info|details|about)\s+(this|that)\s+(property|listing)",
            r"\bfull details? of\b",
        ],
        keywords=["property details", "prop-"],
    ),
    IntentSpec(
        "view_neighborhoods",
        patterns=[
            r"\b(tell me about|info on|about|describe)\s+(the\s+)?(neighborhood|locality|area)\s+\w+",
            r"\bwhat'?s\s+(\w+\s+)?like\s+(in|as a neighborhood)",
            r"\b(compare|comparing)\s+(neighborhoods?|localities|areas?)",
            r"\b(neighborhood|locality|area)\s+(guide|overview|info)",
            r"\babout\s+(vesu|adajan|pal|athwa|citylight|ghod\s*dod)",
        ],
        keywords=["neighborhood", "locality", "area"],
    ),
    IntentSpec(
        "view_projects",
        patterns=[
            r"\b(new|upcoming|ongoing)\s+(projects?|developments?|launches?)\b",
            r"\b(builder|developer)\s+projects?\b",
            r"\b(under\s+construction|ready\s+to\s+move)\s+(projects?|properties?)",
            r"\b(show|view|list)\s+(projects?|developments?)",
        ],
        keywords=["projects", "new launches", "under construction"],
    ),
    IntentSpec(
        "emi_calc",
        patterns=[
            r"\b(emi|installment)\s+(for|on|of|calculation|calc|estimate)",
            r"\bcalculate\s+(my\s+)?(emi|loan|installment)",
            r"\bhome\s+loan\s+(emi|calc(?:ulator)?|estimate)",
            r"\b(monthly\s+)?payment\s+(for|on)\s+\w*\s*(loan|property|mortgage)",
        ],
        keywords=["emi", "loan calculator", "monthly installment"],
    ),
    IntentSpec(
        "affordability",
        patterns=[
            r"\b(how much|what)\s+(home|house|property|loan)\s+can\s+i\s+afford\b",
            r"\bafford(?:able|ability)\s+(budget|range|calculator|check)",
            r"\bmaximum\s+(loan|budget|property)\b.{0,15}(salary|income)",
            r"\b(my|with)\s+(salary|income)\s+(of\s+)?\d",
        ],
        keywords=["afford", "affordability", "what budget"],
    ),
    IntentSpec(
        "schedule_viewing",
        patterns=[
            r"\b(book|schedule|arrange|set\s+up|fix)\s+(a\s+)?(viewing|visit|site\s+visit|tour|inspection)",
            r"\b(viewing|visit|site\s+visit|tour)\s+(for|of|to)\s+(this|prop-?\d+|the\s+property)",
            r"\b(visit|view|see|tour)\s+(the\s+)?(property|flat|villa|apartment|listing)",
            r"\bwhen\s+can\s+i\s+(visit|see|view|tour)\b",
            r"\bsite\s+visit\b",
            r"\bi\s+(want|would\s+like)\s+to\s+(visit|see|view|tour)",
        ],
        keywords=["schedule viewing", "site visit", "book a visit", "schedule a viewing", "viewing for"],
    ),
    IntentSpec(
        "view_viewings",
        patterns=[
            r"\b(my|upcoming|scheduled)\s+(viewings?|visits?|site\s+visits?|tours?)",
            r"\b(view|show|list)\s+(my\s+)?(viewings?|scheduled\s+visits?)",
            r"\bwhat'?s\s+on\s+my\s+(viewing|visit)\s+(schedule|list)",
        ],
        keywords=["my viewings", "scheduled visits"],
    ),
    IntentSpec(
        "saved_searches",
        patterns=[
            r"\b(my\s+)?(saved|favourite|favorite)\s+(searches?|alerts?|listings?)\b",
            r"\b(show|view|list)\s+(my\s+)?(saved\s+searches?|alerts?)",
            r"\bnew\s+(matches?|results?)\s+for\s+(my\s+)?(search|alert)",
        ],
        keywords=["saved searches", "alerts", "favourites"],
    ),
    IntentSpec(
        "market_trends",
        patterns=[
            r"\b(market|price)\s+(trends?|movement|analysis|report)",
            r"\b(how|where)\s+(are\s+)?prices?\s+(going|moving|trending|heading)",
            r"\b(price|rent)\s+(per\s+sq\s*ft|psf)\s+(in|for)\s+\w+",
            r"\b(rates?|price)\s+(in|of|for)\s+(vesu|adajan|pal|athwa|citylight)",
            r"\bproperty\s+rates?\s+(in|of|for)",
        ],
        keywords=["market trends", "price per sqft", "property rates"],
    ),
    IntentSpec(
        "compare_properties",
        patterns=[
            r"\bcompare\s+(these\s+)?(properties?|listings?|flats?|villas?)",
            r"\bcomparison\s+(between|of)\s+(properties?|listings?)",
            r"\bside[\s-]by[\s-]side\b",
            r"\bvs\s+",
        ],
        keywords=["compare", "comparison", "side by side"],
    ),
    IntentSpec(
        "documents_checklist",
        patterns=[
            r"\b(documents?|paperwork|paper-work|papers)\s+(needed|required|checklist|for|to)\s+(to\s+)?(buy|rent|registration|sale|purchase)",
            r"\bwhat\s+(documents?|papers?|paperwork)\s+(do\s+i\s+need|are\s+required)\b",
            r"\bdocuments?\s+do\s+i\s+need\b",
            r"\b(registration|registry|sale\s+deed)\s+(documents?|requirements?|checklist)",
            r"\bdue\s+diligence\s+(checklist|documents?)",
            r"\bchecklist\s+(for|to)\s+(buy(?:ing)?|rent(?:ing)?|purchas(?:e|ing))",
        ],
        keywords=["documents", "paperwork", "checklist", "registration", "paper work"],
    ),
    IntentSpec(
        "talk_to_agent",
        patterns=[
            r"\b(speak|talk|connect|message)\s+(to\s+)?(an?\s+)?(agent|broker|relationship\s+manager|rm|sales)",
            r"\b(real|human|live)\s+(agent|person|broker)",
            r"\bcontact\s+(an?\s+)?(agent|broker)",
        ],
        keywords=["agent", "broker", "human help"],
    ),
]


# ─── Entity extraction ─────────────────────────────────────
NEIGHBORHOODS = ["vesu", "adajan", "pal", "athwa", "citylight", "ghod dod", "ghod-dod", "ghoddod"]


def extract_bhk(text: str) -> Optional[int]:
    """Extract bedroom count: '2 BHK', '2-BHK', '2bhk', 'two bedroom'."""
    t = text.lower()
    m = re.search(r"\b(\d+)\s*[-\s]?\s*(bhk|bedroom|bedrooms|bed)\b", t)
    if m:
        return int(m.group(1))
    word_map = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    for w, n in word_map.items():
        if re.search(rf"\b{w}\s+(bhk|bedroom|bed)\b", t):
            return n
    return None


def extract_neighborhood(text: str) -> Optional[str]:
    t = text.lower()
    for n in NEIGHBORHOODS:
        if n in t:
            # normalize ghod dod variants
            if "ghod" in n:
                return "Ghod Dod Road"
            return n.title()
    return None


def extract_budget(text: str) -> Optional[dict]:
    """Extract 'under 50 lakh', '1 crore', '25k', '₹15000', '12 lakh - 18 lakh'."""
    t = text.lower().replace(",", "")

    def parse_amount(numstr: str, unit: str) -> int:
        n = float(numstr)
        u = unit.lower()
        if u.startswith("cr") or u.startswith("crore"):
            return int(n * 10000000)
        if u in ("l", "lac", "lacs", "lakh", "lakhs"):
            return int(n * 100000)
        if u == "k":
            return int(n * 1000)
        return int(n)

    # range: "X to Y unit" or "X-Y unit"
    rng = re.search(r"(\d+(?:\.\d+)?)\s*(?:to|-|–)\s*(\d+(?:\.\d+)?)\s*(crore|cr|lakh|lakhs|lac|lacs|l|k)\b", t)
    if rng:
        lo = parse_amount(rng.group(1), rng.group(3))
        hi = parse_amount(rng.group(2), rng.group(3))
        return {"min": lo, "max": hi}

    # under / below / less than
    under = re.search(r"\b(under|below|less than|max(?:imum)?|upto|up to|within)\s+(\d+(?:\.\d+)?)\s*(crore|cr|lakh|lakhs|lac|lacs|l|k)?\b", t)
    if under:
        amt = parse_amount(under.group(2), under.group(3) or "")
        return {"max": amt}

    # above / over
    over = re.search(r"\b(above|over|more than|min(?:imum)?|from)\s+(\d+(?:\.\d+)?)\s*(crore|cr|lakh|lakhs|lac|lacs|l|k)?\b", t)
    if over:
        amt = parse_amount(over.group(2), over.group(3) or "")
        return {"min": amt}

    # single budget: "1 crore", "50 lakh"
    single = re.search(r"\b(\d+(?:\.\d+)?)\s*(crore|cr|lakh|lakhs|lac|lacs)\b", t)
    if single:
        amt = parse_amount(single.group(1), single.group(2))
        return {"approx": amt}

    return None


def extract_property_id(text: str) -> Optional[str]:
    m = re.search(r"\bprop-?(\d{4,6})\b", text.lower())
    if m:
        return f"PROP-{m.group(1)}"
    return None


def extract_salary(text: str) -> Optional[int]:
    """Extract salary like '1.5 lakh per month' / '15 lpa' / '120000 monthly'."""
    t = text.lower().replace(",", "")
    # X lpa
    lpa = re.search(r"\b(\d+(?:\.\d+)?)\s*lpa\b", t)
    if lpa:
        return int(float(lpa.group(1)) * 100000 / 12)
    # X lakh per month
    lpm = re.search(r"\b(\d+(?:\.\d+)?)\s*(lakh|lakhs|lac|lacs|l)\s+(per\s+month|/month|monthly|a month)", t)
    if lpm:
        return int(float(lpm.group(1)) * 100000)
    # plain monthly figure
    m = re.search(r"\b(\d{4,7})\s*(?:per\s+month|/month|monthly|a month)", t)
    if m:
        return int(m.group(1))
    return None


# ─── Classifier ────────────────────────────────────────────
@dataclass
class Classification:
    intent: str
    confidence: float
    entities: dict


def classify(text: str) -> Classification:
    raw = text
    text_lc = text.lower().strip()

    scores: dict[str, float] = {}
    for spec in INTENTS:
        score = 0.0
        for p in spec.patterns:
            if re.search(p, text_lc, re.IGNORECASE):
                score += 2.0
        for kw in spec.keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text_lc):
                score += 0.6
        if score > 0:
            scores[spec.name] = score

    # Bare property id → property_detail, but only if no stronger intent already scored
    if extract_property_id(text):
        if not scores or max(scores.values()) < 2.0:
            scores["property_detail"] = max(scores.get("property_detail", 0), 3.0)
        else:
            # Property ID alongside another intent — keep that intent
            scores["property_detail"] = scores.get("property_detail", 0) + 0.5

    if not scores:
        intent, conf = "unknown", 0.0
    else:
        intent = max(scores, key=scores.get)
        top = scores[intent]
        rest = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0.1
        conf = min(1.0, top / (top + rest))

    entities = {
        "bhk":          extract_bhk(raw),
        "neighborhood": extract_neighborhood(raw),
        "budget":       extract_budget(raw),
        "property_id":  extract_property_id(raw),
        "salary":       extract_salary(raw),
    }
    return Classification(intent=intent, confidence=round(conf, 2), entities=entities)
