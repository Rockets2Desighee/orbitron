# sat-ingest (skeleton)

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Example: list a few Sentinel-2 L2A items from Earth Search
sat search --collections sentinel-2-l2a --limit 3

# Example: download first item (all assets) in July 2024 over a bounding box
sat download --collections sentinel-2-l2a \
  --time 2024-07-01/2024-07-02 \
  --bbox -122.6,37.6,-122.2,37.9 \
  --limit 1