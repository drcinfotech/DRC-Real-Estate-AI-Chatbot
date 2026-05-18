"""Data catalog — loads listings from JSON."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


DATA_DIR = Path(__file__).parent.parent / "data"


class Catalog:
    def __init__(self):
        with open(DATA_DIR / "listings.json", "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def properties(self, listing_type: Optional[str] = None) -> list[dict]:
        items = list(self._data["properties"])
        if listing_type:
            items = [p for p in items if p["listing_type"] == listing_type]
        return items

    def property(self, prop_id: str) -> Optional[dict]:
        for p in self._data["properties"]:
            if p["id"] == prop_id:
                return p
        return None

    def neighborhoods(self) -> list[dict]:
        return list(self._data["neighborhoods"])

    def neighborhood(self, name: str) -> Optional[dict]:
        n = name.lower()
        for nb in self._data["neighborhoods"]:
            if nb["name"].lower() == n or nb["id"] == n:
                return nb
        return None

    def projects(self) -> list[dict]:
        return list(self._data["projects"])

    def saved_searches(self) -> list[dict]:
        return list(self._data["saved_searches"])

    def viewings(self) -> list[dict]:
        return list(self._data["viewings"])


catalog = Catalog()
