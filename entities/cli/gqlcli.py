import json
import logging

import click
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

from cli import gql_schema as schema


@click.group()
@click.option(
    "--endpoint",
    type=str,
    default="http://localhost:8008/graphql",
    required=True,
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug output",
)
@click.pass_context
def cli(ctx, endpoint, debug):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    ctx.ensure_object(dict)
    ctx.obj["endpoint"] = endpoint


@cli.group()
def samples():
    pass

@samples.command("list")
@click.pass_context
def list_samples(ctx):
    endpoint = HTTPEndpoint(ctx.obj["endpoint"])
    op = Operation(schema.Query)  # note 'schema.'

    # fetch all samples and all sample fields
    samples = op.get_all_samples()
    samples.id()
    samples.name()
    samples.location()

    # Print the query if we're in debug mode
    logging.debug(op)

    # Call the endpoint:
    data = endpoint(op)
    print(json.dumps(data["data"]["getAllSamples"], indent=4))


if __name__ == "__main__":
    cli()
