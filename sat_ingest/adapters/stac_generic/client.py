from __future__ import annotations
from typing import Iterable, Optional, Sequence, Dict
from sat_ingest.core.adapters.base import CatalogAdapter
from sat_ingest.core.search import SearchParams
from sat_ingest.core.models import Item, Asset
from sat_ingest.core.http import HttpClient
from .mapper import map_stac_item
import os

STAC_DEFAULT_URL = os.environ.get("STAC_URL", "https://earth-search.aws.element84.com/v1") # Just a placeholder.

class StacGenericAdapter(CatalogAdapter):
    name = "Generic STAC"

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or STAC_DEFAULT_URL
        self.http = HttpClient()

    def search(self, params: SearchParams) -> Iterable[Item]:
        url = f"{self.base_url}/search"
        payload = params.to_stac_payload()
        resp = self.http.post(url, json=payload).json()
        for feat in resp.get("features", []):
            yield map_stac_item(feat)
        # NOTE: add proper STAC paging ("next" links) later.

    def item(self, item_id: str) -> Optional[Item]:
        url = f"{self.base_url}/collections/*/items/{item_id}"
        # Some STAC APIs require collection; for now we try /items/{id}
        alt = f"{self.base_url}/items/{item_id}"
        for candidate in (url, alt):
            try:
                resp = self.http.get(candidate)
                return map_stac_item(resp.json())
            except Exception:
                continue
        return None

    def download(self, item: Item, asset_keys: Optional[Sequence[str]] = None, **kwargs) -> Dict[str, Asset]:
        selected = asset_keys or list(item.assets.keys())
        out: Dict[str, Asset] = {}
        for k in selected:
            asset = item.assets[k]
            # For demo: download to ./data/<collection>/<id>/<key>
            dest_key = f"{item.collection}/{item.id}/{k}"
            dest_path = os.path.join("data", dest_key)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            self.http.stream_download(asset.href, dest_path)
            asset.local_path = dest_path
            out[k] = asset
        return out