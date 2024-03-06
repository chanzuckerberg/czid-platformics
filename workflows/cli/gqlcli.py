#!/usr/bin/env python3

"""
Simple CLI for interacting with the GraphQL API
"""

import json
import logging

import click
from datetime import datetime
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

from cli import gql_schema as schema


@click.group()
@click.option(
    "--endpoint",
    type=str,
    default="http://localhost:8042/graphql",
    required=True,
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug output",
)
@click.option(
    "--token",
    type=str,
    help="Auth token to use for requests",
    envvar="PLATFORMICS_AUTH_TOKEN",
)
@click.pass_context
def cli(ctx: click.Context, endpoint: str, debug: bool, token: str) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    ctx.ensure_object(dict)
    ctx.obj["endpoint"] = endpoint
    ctx.obj["auth_token"] = token


def get_headers(ctx: click.Context) -> dict[str, str]:
    if ctx.obj["auth_token"]:
        return {"Authorization": f"Bearer {ctx.obj['auth_token']}"}
    return {}


@cli.group()
def samples() -> None:
    pass


@samples.command("add_run")
@click.pass_context
def add_run(ctx: click.Context) -> None:
    endpoint = HTTPEndpoint(ctx.obj["endpoint"])
    op = Operation(schema.Mutation)  # note 'schema.'

    # create the GQL query to fetch all samples and all sample fields
    op.create_run(
        input=schema.RunCreateInput(
            collection_id=444,
            started_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            ended_at=None,
            execution_id="cli-execution-id",
            outputs_json=None,
            inputs_json="{}",
            status="RUNNING",
        )
    ).__fields__()

    # Print the query if we're in debug mode
    logging.debug(op)

    # Call the endpoint:
    data = endpoint(op, extra_headers=get_headers(ctx))
    breakpoint()
    print(json.dumps(data["data"]["samples"], indent=4))


@cli.group()
def auth() -> None:
    pass


if __name__ == "__main__":
    cli()
