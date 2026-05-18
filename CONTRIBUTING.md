# Contributing to Property Assistant

Thanks for your interest! This is a demo of conversational AI for the real estate / property domain, so contributions are welcome — but **fair-housing-critical code paths have extra rules** that apply on top of normal code-review.

## Code of conduct

Be kind. Disagree on technical merits, not on people. Maintainers reserve the right to close issues and PRs that violate this.

## Quick start for contributors

```bash
git clone https://github.com/drcinfotech/Real-Estate-AI-Chatbot.git
cd Real-Estate-AI-Chatbot

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest -v       # must be 58/58 green before you start

# Frontend
cd ../frontend
npm install
npm run dev
```

## What we accept

✅ **Good contributions:**

- New intents with corresponding tests
- New block renderers in `Blocks.jsx` with corresponding Pydantic models
- New fair-housing patterns — with both a positive test and a no-false-positive test
- More fictional property listings, neighborhoods, or projects (must be invented, not real)
- Documentation, README improvements, screenshots
- Accessibility improvements (keyboard nav, ARIA, contrast)
- i18n / localization support (Hindi, Gujarati, Tamil, etc)
- Tighter test coverage

❌ **What we do NOT accept:**

- Real real-estate, brokerage, builder, or developer brand names anywhere in the codebase. The CI test `test_no_real_brokerage_brands_in_data` will fail your PR.
- Removing or weakening the fair-housing safety layer
- Anything that helps users filter properties by protected characteristics (religion, caste, community, race, family status, disability, gender, national origin) or coded proxies for these
- Making the bot reveal owner contact details bypassing the agent flow
- Removing or relaxing prompt-injection / social-engineering blocks
- Real RERA IDs, real property addresses, or any data that could be confused for real listings
- Adding personal API keys or credentials
- Code that connects to real MLS, RERA portals, or property databases without explicit opt-in and clear documentation of risks
- Replacing the generic "Property Assistant" name with an unverified brand name

## Fair-housing-rule changes (require extra review)

Any PR that modifies the following files **must** include test coverage and a written rationale in the PR description:

- `backend/app/safety.py` — fair-housing, privacy, and social-engineering detection
- `backend/app/chatbot.py` — the safety-first dispatch logic
- `backend/data/*.json` — particularly anything that could be construed as targeting a community
- The EMI/affordability calculator math (errors here could mislead users financially)

Maintainers will request changes to any safety-weakening PR unless the justification is strong. When in doubt about whether a query is asking for "filtering" vs "discriminatory filtering", the safe default is to **refuse and explain neutral alternatives**.

## Style

- Python: PEP 8, type hints on public functions, docstrings on modules
- JS/JSX: 2-space indent, prefer functional components, hooks for state
- Commits: imperative present tense ("Add X", "Fix Y"), not past tense
- One logical change per PR

## Reporting a security issue

For anything that looks like a real security issue (not just a demo limitation), please email the maintainers privately rather than opening a public issue.
