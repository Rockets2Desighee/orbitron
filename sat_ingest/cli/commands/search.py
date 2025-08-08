import json
import click
from sat_ingest.adapters.stac_generic.client import StacGenericAdapter
from sat_ingest.core.search import SearchParams

@click.command()
@click.option("--collections", multiple=True, help="STAC collections")
@click.option("--time", help="ISO range, e.g. 2024-07-01/2024-07-31")
@click.option("--bbox", help="minx,miny,maxx,maxy")
@click.option("--limit", type=int, default=10)
def search_cmd(collections, time, bbox, limit):
    bbox_list = [float(x) for x in bbox.split(",")] if bbox else None
    params = SearchParams(collections=list(collections) or None, time=time, bbox=bbox_list, limit=limit)
    adapter = StacGenericAdapter()
    for item in adapter.search(params):
        click.echo(json.dumps({"id": item.id, "collection": item.collection, "datetime": item.datetime}))