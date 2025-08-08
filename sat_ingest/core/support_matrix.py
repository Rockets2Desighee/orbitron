from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class SourceChoice:
    adapter: str  # entry name, e.g., "stac_generic"
    reason: str

_DEFAULT = {
    ("sentinel-2", "L2A"): SourceChoice(adapter="stac_generic", reason="Public STAC on Earth Search is fast and free"),
    ("landsat-8", "L2"): SourceChoice(adapter="stac_generic", reason="Earth Search/LPC"),
}

class SupportMatrix:
    def __init__(self, overrides: dict | None = None):
        self._rules = {**_DEFAULT, **(overrides or {})}

    def resolve(self, satellite: str, product: str) -> SourceChoice:
        key = (satellite.lower(), product.upper())
        if key in self._rules:
            return self._rules[key]
        # naive default; refined as we add adapters
        return SourceChoice(adapter="stac_generic", reason="Fallback to STAC where available")