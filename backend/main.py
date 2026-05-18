"""FastAPI entry point for the Real Estate & Property AI Chatbot."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.catalog import catalog
from app.chatbot import engine
from app.models import ChatRequest, ChatResponse
from app.sessions import store

app = FastAPI(
    title="Real Estate AI Chatbot — Property Assistant",
    description=(
        "A demo conversational AI for the real estate & property industry. Includes intent classification, "
        "fair-housing guardrails, financial-disclaimer enforcement, and rich response blocks for listings, "
        "neighborhoods, projects, EMI estimates, affordability checks, viewings, and document checklists. "
        "NOT a licensed real estate brokerage."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status":       "ok",
        "properties":   len(catalog.properties()),
        "neighborhoods": len(catalog.neighborhoods()),
        "projects":     len(catalog.projects()),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session = store.get_or_create(req.session_id)
    return engine.respond(req.message, session)


@app.get("/properties")
def list_properties(listing_type: str | None = None):
    return catalog.properties(listing_type=listing_type)


@app.get("/properties/{prop_id}")
def get_property(prop_id: str):
    p = catalog.property(prop_id)
    if not p:
        return {"error": "not_found", "id": prop_id}
    return p


@app.get("/neighborhoods")
def list_neighborhoods():
    return catalog.neighborhoods()


@app.get("/projects")
def list_projects():
    return catalog.projects()


@app.get("/viewings")
def list_viewings():
    return catalog.viewings()


@app.get("/saved-searches")
def list_saved_searches():
    return catalog.saved_searches()


@app.get("/")
def root():
    return {
        "name":       "Real Estate AI Chatbot — Property Assistant",
        "version":    app.version,
        "docs":       "/docs",
        "disclaimer": "Demo only. Not a licensed real estate brokerage or RBI-regulated lender.",
    }
