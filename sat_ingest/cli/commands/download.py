import click
from sat_ingest.adapters.stac_generic.client import StacGenericAdapter
from sat_ingest.core.search import SearchParams

@click.command()
@click.option("--collections", multiple=True, required=True)
@click.option("--time", required=True)
@click.option("--bbox", required=False)
@click.option("--limit", type=int, default=1)
@click.option("--assets", help="Comma-separated asset keys (default all)")
def download_cmd(collections, time, bbox, limit, assets):
    bbox_list = [float(x) for x in bbox.split(",")] if bbox else None
    asset_keys = [a.strip() for a in assets.split(",")] if assets else None
    params = SearchParams(collections=list(collections), time=time, bbox=bbox_list, limit=limit)
    adapter = StacGenericAdapter()
    for item in adapter.search(params):
        result = adapter.download(item, asset_keys=asset_keys)
        for k, asset in result.items():
            click.echo(f"Downloaded {k} -> {asset.local_path}")