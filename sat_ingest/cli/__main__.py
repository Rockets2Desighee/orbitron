import click
from .commands.search import search_cmd
from .commands.download import download_cmd

@click.group()
def cli():
    """sat — satellite ingestion CLI"""

cli.add_command(search_cmd, name="search")
cli.add_command(download_cmd, name="download")

def main():
    cli()

if __name__ == "__main__":
    main()