from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable

@dataclass
class SearchParams:
    collections: Optional[list[str]] = None
    time: Optional[str] = None  # ISO8601 range, e.g. "2024-01-01/2024-01-31"
    intersects: Optional[dict] = None  # GeoJSON geometry
    bbox: Optional[list[float]] = None  # [minx, miny, maxx, maxy]
    limit: int = 100
    query: Optional[dict] = None  # provider-specific filters, e.g. {"eo:cloud_cover": {"lt": 20}}

    def to_stac_payload(self) -> dict:
        body = {k: v for k, v in {
            "collections": self.collections,
            "datetime": self.time,
            "intersects": self.intersects,
            "bbox": self.bbox,
            "limit": self.limit,
            "query": self.query,
        }.items() if v is not None}
        return body