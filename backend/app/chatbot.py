"""
Real Estate chatbot engine.

Flow:
  1. Safety check first — fair-housing, privacy, social-engineering
  2. Otherwise, classify intent
  3. Dispatch to handler
  4. Return rich blocks
"""
from __future__ import annotations

from .catalog import catalog
from .intents import Classification, classify
from .safety import (
    check_safety,
    build_fair_housing_block,
    build_privacy_block,
    build_social_engineering_block,
)
from .sessions import Session


# ─── Block helpers ─────────────────────────────────────────
def _text(content: str) -> dict:
    return {"type": "text", "content": content}


def _disclaimer(content: str) -> dict:
    return {"type": "disclaimer", "content": content}


def _filter_properties(listing_type: str | None, bhk: int | None,
                       neighborhood: str | None, budget: dict | None) -> list[dict]:
    items = catalog.properties(listing_type=listing_type)
    if bhk is not None:
        items = [p for p in items if p.get("bhk") == bhk]
    if neighborhood:
        items = [p for p in items if p["neighborhood"].lower() == neighborhood.lower()]
    if budget:
        if "max" in budget:
            items = [p for p in items if p["price"] <= budget["max"]]
        if "min" in budget:
            items = [p for p in items if p["price"] >= budget["min"]]
        if "approx" in budget:
            # ±20% window around target
            lo, hi = budget["approx"] * 0.8, budget["approx"] * 1.2
            items = [p for p in items if lo <= p["price"] <= hi]
    return items


def _compute_emi(principal: float, annual_rate_pct: float, years: int) -> dict:
    r = annual_rate_pct / 100 / 12
    n = years * 12
    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    total = emi * n
    return {
        "emi": round(emi, 2),
        "total_payable": round(total, 2),
        "total_interest": round(total - principal, 2),
    }


# ─── Intent handlers ───────────────────────────────────────
def _handle_greeting(_s: Session):
    return [
        _text(
            "Hi 👋 — I'm your Property Assistant. I can search for homes to buy or rent, "
            "explore neighborhoods, check new projects, calculate EMIs, schedule viewings, "
            "and walk you through the paperwork. What are you looking for today?"
        )
    ], ["3 BHK for sale in Vesu", "2 BHK rentals in Adajan", "EMI calculator", "Show new projects"]


def _handle_goodbye(_s: Session):
    return [_text("Best of luck with the property search. Come back any time.")], []


def _handle_thanks(_s: Session):
    return [_text("Happy to help. Anything else you'd like to explore?")], \
           ["More listings", "Neighborhood info", "Schedule a viewing"]


def _handle_search(c: Classification, s: Session, listing_type: str):
    items = _filter_properties(listing_type, c.entities["bhk"], c.entities["neighborhood"], c.entities["budget"])
    if not items:
        criteria = []
        if c.entities["bhk"]:          criteria.append(f"{c.entities['bhk']} BHK")
        if c.entities["neighborhood"]: criteria.append(f"in {c.entities['neighborhood']}")
        if c.entities["budget"]:
            b = c.entities["budget"]
            if "max" in b: criteria.append(f"under ₹{b['max']:,}")
        crit = " ".join(criteria) if criteria else "matching your criteria"
        return [_text(
            f"I couldn't find any {listing_type} listings {crit} in this demo's catalog. "
            "Try adjusting BHK, neighborhood, or budget. The demo has 6 fictional listings across Vesu, Adajan, Pal, Athwa, Ghod Dod Road, and Citylight."
        )], ["3 BHK in Vesu", "2 BHK in Adajan", "Villas in Pal", "Show all listings"]

    # Save filters for follow-ups
    s.last_filters = {"listing_type": listing_type, **{k: v for k, v in c.entities.items() if v}}
    label = "for sale" if listing_type == "sale" else "for rent"
    return [
        _text(f"I found **{len(items)} {label} listings** matching your criteria:"),
        {"type": "property_list", "title": f"Listings {label}", "items": items, "total": len(items)},
    ], ["Schedule a viewing", "Calculate EMI", "Compare these", "Save this search"]


def _handle_search_buy(c: Classification, s: Session):
    return _handle_search(c, s, "sale")


def _handle_search_rent(c: Classification, s: Session):
    return _handle_search(c, s, "rent")


def _handle_search_commercial(_c: Classification, _s: Session):
    items = [p for p in catalog.properties() if p["type"] in ("Office", "Showroom", "Warehouse", "Retail")]
    return [
        _text(f"Here are **{len(items)} commercial listings** in Surat:"),
        {"type": "property_list", "title": "Commercial listings", "items": items, "total": len(items)},
    ], ["Office space", "Showroom", "Schedule a viewing"]


def _handle_property_detail(c: Classification, s: Session):
    pid = c.entities.get("property_id") or s.last_property_id
    if not pid:
        return [_text(
            "Which property would you like details on? You can paste a property ID (like PROP-21089), "
            "or start a search and click one of the results."
        )], ["3 BHK in Vesu", "2 BHK rentals", "Show all listings"]

    p = catalog.property(pid)
    if not p:
        return [_text(f"I couldn't find property **{pid}** in the catalog. Please double-check the ID.")], []

    s.last_property_id = pid
    return [
        _text(f"Here are the full details on **{p['title']}**:"),
        {"type": "property_detail", "property": p},
    ], ["Schedule a viewing", "Calculate EMI for this", "Compare with similar", "Talk to agent"]


def _handle_view_neighborhoods(c: Classification, _s: Session):
    nb_name = c.entities.get("neighborhood")
    if nb_name:
        nb = catalog.neighborhood(nb_name)
        if nb:
            return [
                _text(f"Here's an overview of **{nb['name']}**:"),
                {"type": "neighborhood", "title": f"About {nb['name']}", "items": [nb]},
            ], ["Properties here", "Market trends", "Compare neighborhoods"]

    items = catalog.neighborhoods()
    return [
        _text(f"Here are **{len(items)} neighborhoods** in Surat covered in this demo:"),
        {"type": "neighborhood", "title": "Neighborhoods", "items": items},
    ], ["Properties in Vesu", "Properties in Adajan", "Market trends"]


def _handle_view_projects(_c: Classification, _s: Session):
    items = catalog.projects()
    return [
        _text(f"There are **{len(items)} active projects** from RERA-registered developers:"),
        {"type": "project", "title": "Active projects", "items": items},
        _disclaimer(
            "Project details are illustrative. Always verify the latest RERA registration, approvals, "
            "and completion status on the official RERA portal of the state before booking."
        ),
    ], ["Properties in these projects", "Schedule a site visit", "Affordability check"]


def _handle_emi(c: Classification, s: Session):
    # Use last viewed property if available
    pid = c.entities.get("property_id") or s.last_property_id
    p = catalog.property(pid) if pid else None
    if p and p["listing_type"] == "sale":
        price = p["price"]
        property_label = p["title"]
    else:
        price = 10000000   # ₹1 cr fictional default
        property_label = "a ₹1 crore property (default — pick a listing for a specific quote)"

    down = int(price * 0.20)       # 20% down
    loan = price - down
    rate = 8.5                     # illustrative
    years = 20
    res = _compute_emi(loan, rate, years)

    return [
        _text(
            f"Here's a sample EMI breakdown for **{property_label}** assuming a 20% down payment, "
            f"{rate:.1f}% interest, and a {years}-year tenure:"
        ),
        {
            "type":            "emi",
            "property_price":  int(price),
            "down_payment":    down,
            "loan_amount":     loan,
            "interest_rate":   rate,
            "tenure_years":    years,
            "emi":             res["emi"],
            "total_interest":  res["total_interest"],
            "total_payable":   res["total_payable"],
        },
        _disclaimer(
            "This is an illustrative estimate, not a loan offer. Actual EMI depends on your bank's interest rate, "
            "credit profile, processing fees, insurance, and tenure approval. Banks are regulated by the RBI — "
            "always compare offers and read the sanction letter carefully."
        ),
    ], ["Affordability check", "Different tenure", "Different down payment", "Talk to an agent"]


def _handle_affordability(c: Classification, _s: Session):
    salary = c.entities.get("salary")
    if not salary:
        return [_text(
            "I can estimate the property budget you can afford. What's your **monthly income**? "
            "You can say something like *'my salary is 1.5 lakh per month'* or *'income is 15 LPA'*. "
            "If you have other EMIs or major obligations, mention those too."
        )], ["My salary is 1 lakh per month", "Income is 12 LPA", "Income is 50000/month"]

    obligations = 0     # in a real impl, capture from message
    # FOIR (Fixed Obligations to Income Ratio) approach — banks typically cap at 50%
    max_emi = max((salary - obligations) * 0.50, 0)
    # Reverse-EMI: loan amount from EMI at 8.5%, 20 years
    r = 8.5 / 100 / 12
    n = 20 * 12
    estimated_loan = int(max_emi * ((1 + r) ** n - 1) / (r * (1 + r) ** n)) if max_emi > 0 else 0
    # Assume 80% LTV → property = loan / 0.8
    property_budget = int(estimated_loan / 0.8) if estimated_loan else 0

    return [
        _text(
            f"With a monthly income of **₹{salary:,}**, you can typically afford a property of around "
            f"**₹{property_budget:,}** — give or take."
        ),
        {
            "type":                       "affordability",
            "monthly_income":             salary,
            "obligations":                obligations,
            "estimated_loan":             estimated_loan,
            "estimated_property_budget":  property_budget,
            "assumptions": [
                "FOIR cap of 50% (banks may approve 40–60% depending on profile)",
                "Loan tenure of 20 years",
                "Interest rate of 8.5% p.a. (illustrative)",
                "20% down payment (i.e. 80% LTV from bank)",
                "No other ongoing EMIs (adjust if you have them)",
            ],
        },
        _disclaimer(
            "This is a rough back-of-the-envelope estimate, not a loan eligibility decision. "
            "Actual eligibility depends on credit score, employment type, age, co-applicant, and bank policy."
        ),
    ], ["See properties in this range", "Calculate EMI", "Speak to a loan advisor"]


def _handle_schedule_viewing(c: Classification, s: Session):
    pid = c.entities.get("property_id") or s.last_property_id
    if not pid:
        return [_text(
            "Sure — which property would you like to view? Tell me the property ID, "
            "or start a search first."
        )], ["3 BHK in Vesu", "Show all listings"]

    p = catalog.property(pid)
    if not p:
        return [_text(f"I couldn't find property **{pid}**.")], []

    return [
        _text(f"Viewing request received for **{p['title']}**. The listing agent will reach out to confirm a time slot:"),
        {
            "type": "viewing",
            "confirmation": {
                "viewing_id":    "VW-DEMO-001",
                "property_id":   p["id"],
                "property_title": p["title"],
                "neighborhood":  p["neighborhood"],
                "status":        "Pending confirmation",
                "next_step":     "The listing agent will contact you within 2 business hours to fix a time.",
                "demo_only":     True,
            },
        },
        _disclaimer(
            "This is a demo — no actual viewing has been scheduled and no agent has been notified. "
            "In a production system, this would create a real lead and send a notification."
        ),
    ], ["My viewings", "Calculate EMI for this", "Compare with similar"]


def _handle_view_viewings(_c: Classification, _s: Session):
    items = catalog.viewings()
    # enrich with property title
    enriched = []
    for v in items:
        p = catalog.property(v["property_id"])
        enriched.append({**v, "property_title": p["title"] if p else "Unknown"})
    return [
        _text(f"You have **{len(items)} scheduled viewings**:"),
        {"type": "viewing_list", "items": enriched},
    ], ["Schedule another", "Reschedule a viewing", "Cancel a viewing"]


def _handle_saved_searches(_c: Classification, _s: Session):
    items = catalog.saved_searches()
    total_matches = sum(s.get("new_matches", 0) for s in items)
    return [
        _text(
            f"You have **{len(items)} saved searches** with **{total_matches} new matches** since your last visit:"
        ),
        {"type": "saved_search", "items": items},
    ], ["Show new matches", "Create a new alert", "Edit search criteria"]


def _handle_market_trends(c: Classification, _s: Session):
    nb_filter = c.entities.get("neighborhood")
    items = catalog.neighborhoods()
    if nb_filter:
        items = [n for n in items if n["name"].lower() == nb_filter.lower()] or items
    return [
        _text(
            f"Here's the **price-per-sqft snapshot** for the neighborhoods in this demo. "
            "Sale figures are for residential apartments; rent figures are for residential rentals (except where commercial-only)."
        ),
        {
            "type":          "market_trend",
            "title":         "Price trends",
            "neighborhoods": items,
            "period":        "Snapshot, illustrative",
        },
        _disclaimer(
            "Numbers in this demo are illustrative averages, not live market data. For current rates, "
            "consult RERA, registrar's office records, or a local property advisor."
        ),
    ], ["Properties in this range", "Compare neighborhoods", "Affordability check"]


def _handle_compare_properties(_c: Classification, _s: Session):
    # Take a curated comparison set from the catalog
    pool = catalog.properties()
    pick = [pool[0], pool[2]]   # 3 BHK Vesu + 4 BHK villa Pal — both for sale
    return [
        _text("Here's a side-by-side of two strong options I've pulled for comparison:"),
        {
            "type": "compare",
            "properties": pick,
            "attributes": ["price", "bhk", "carpet_sqft", "neighborhood", "type", "age_years", "furnishing", "rera_id"],
        },
    ], ["See more options", "Calculate EMI for these", "Schedule viewings"]


def _handle_documents(c: Classification, _s: Session):
    # Default to buy-side checklist; could be tuned by intent text
    t = c if hasattr(c, "intent") else None
    purpose = "buy"
    items_buy = [
        {"name": "Sale agreement / Agreement to sell", "category": "Transaction", "required": True,
         "note": "Drafted by the seller's lawyer; reviewed by your lawyer before signing"},
        {"name": "Title deed (chain for 30 years preferred)", "category": "Title", "required": True,
         "note": "Verify ownership lineage to the current seller"},
        {"name": "Encumbrance certificate (EC)", "category": "Title", "required": True,
         "note": "From the sub-registrar's office, confirms no outstanding charges"},
        {"name": "RERA registration certificate", "category": "Project", "required": True,
         "note": "For new builds/under-construction projects only"},
        {"name": "Building plan approval", "category": "Approvals", "required": True,
         "note": "From the local municipal corporation"},
        {"name": "Occupancy certificate (OC)", "category": "Approvals", "required": True,
         "note": "Mandatory for completed buildings — confirms it's legal to occupy"},
        {"name": "Completion certificate (CC)", "category": "Approvals", "required": False,
         "note": "Confirms construction matches approved plan"},
        {"name": "Property tax receipts (last 3 years)", "category": "Tax", "required": True,
         "note": "Confirms no arrears"},
        {"name": "Latest utility bills", "category": "Utility", "required": True,
         "note": "Electricity, water — to confirm no unpaid dues"},
        {"name": "Society NOC + share certificate", "category": "Society", "required": True,
         "note": "For apartments in housing societies"},
        {"name": "PAN + Aadhaar of seller and buyer", "category": "KYC", "required": True,
         "note": "Required for registration"},
        {"name": "Stamp duty + registration fee receipts", "category": "Transaction", "required": True,
         "note": "Paid at the time of registration"},
    ]
    return [
        _text(f"Here's a typical **document checklist for a property purchase** in India. Adapt to your state's specific requirements:"),
        {"type": "document_checklist", "purpose": purpose, "items": items_buy},
        _disclaimer(
            "This is a general guide. Document requirements vary by state, property type, and whether the property "
            "is freehold/leasehold or under construction. Engage a local property lawyer for due diligence — "
            "this is the single best investment you'll make in the transaction."
        ),
    ], ["Documents for rental agreement", "Talk to a lawyer", "Verify RERA"]


def _handle_talk_to_agent(_c: Classification, _s: Session):
    return [_text(
        "Sure — I can connect you to a listing agent. For specific properties you've shown interest in, "
        "the agent named on the listing is the right person. For new searches, I can route you to a "
        "RERA-registered agent in your preferred neighborhood. Want me to do that?"
    )], ["Yes — connect me", "Show my saved searches", "Schedule a viewing"]


def _handle_unknown(_c: Classification, _s: Session):
    return [_text(
        "I'm not sure I caught that. I can search properties to buy or rent, explain neighborhoods, show projects, "
        "calculate EMIs, check affordability, schedule viewings, or list paperwork. Try a button below."
    )], ["3 BHK for sale", "2 BHK rentals", "EMI calculator", "Neighborhoods"]


# ─── Engine ────────────────────────────────────────────────
class ChatbotEngine:
    def respond(self, message: str, session: Session) -> dict:
        # 1️⃣ Safety check first
        safety = check_safety(message)
        if safety.flag == "fair_housing":
            return {
                "session_id": session.session_id,
                "intent":     "fair_housing_block",
                "confidence": 1.0,
                "blocks":     [build_fair_housing_block()],
                "suggestions": ["Search by budget instead", "Search by BHK & neighborhood", "Filter by amenities"],
                "safety_flag": "fair_housing",
            }
        if safety.flag == "privacy":
            return {
                "session_id": session.session_id,
                "intent":     "privacy_block",
                "confidence": 1.0,
                "blocks":     [build_privacy_block()],
                "suggestions": ["Schedule a viewing", "Message the listing agent", "Show property details"],
                "safety_flag": "privacy",
            }
        if safety.flag == "social_engineering":
            return {
                "session_id": session.session_id,
                "intent":     "social_engineering_blocked",
                "confidence": 1.0,
                "blocks":     [build_social_engineering_block()],
                "suggestions": ["Show listings", "Neighborhoods", "EMI calculator"],
                "safety_flag": "social_engineering",
            }

        # 2️⃣ Classify intent
        c = classify(message)
        session.last_intent = c.intent
        session.history.append({"role": "user", "text": message})

        # If a property_id was extracted, remember it for follow-ups
        if c.entities.get("property_id"):
            session.last_property_id = c.entities["property_id"]

        handler_map = {
            "greeting":            lambda: _handle_greeting(session),
            "goodbye":             lambda: _handle_goodbye(session),
            "thanks":              lambda: _handle_thanks(session),
            "search_buy":          lambda: _handle_search_buy(c, session),
            "search_rent":         lambda: _handle_search_rent(c, session),
            "search_commercial":   lambda: _handle_search_commercial(c, session),
            "property_detail":     lambda: _handle_property_detail(c, session),
            "view_neighborhoods":  lambda: _handle_view_neighborhoods(c, session),
            "view_projects":       lambda: _handle_view_projects(c, session),
            "emi_calc":            lambda: _handle_emi(c, session),
            "affordability":       lambda: _handle_affordability(c, session),
            "schedule_viewing":    lambda: _handle_schedule_viewing(c, session),
            "view_viewings":       lambda: _handle_view_viewings(c, session),
            "saved_searches":      lambda: _handle_saved_searches(c, session),
            "market_trends":       lambda: _handle_market_trends(c, session),
            "compare_properties":  lambda: _handle_compare_properties(c, session),
            "documents_checklist": lambda: _handle_documents(c, session),
            "talk_to_agent":       lambda: _handle_talk_to_agent(c, session),
        }
        handler = handler_map.get(c.intent, lambda: _handle_unknown(c, session))
        blocks, suggestions = handler()

        return {
            "session_id":  session.session_id,
            "intent":      c.intent,
            "confidence":  c.confidence,
            "blocks":      blocks,
            "suggestions": suggestions,
            "safety_flag": None,
        }


engine = ChatbotEngine()
