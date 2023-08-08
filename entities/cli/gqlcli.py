#!/usr/bin/env python3
import json
import logging

import click
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation
from security.token_auth import create_token
from api.core.settings import Settings

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
@click.option(
    "--token",
    type=str,
    help="Auth token to use for requests",
    envvar="PLATFORMICS_AUTH_TOKEN",
)
@click.pass_context
def cli(ctx, endpoint, debug, token):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    ctx.ensure_object(dict)
    ctx.obj["endpoint"] = endpoint
    ctx.obj["auth_token"] = token

def get_headers(ctx):
    if ctx.obj["auth_token"]:
        return {"Authorization": f"Bearer {ctx.obj['auth_token']}"}
    return {}

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
    data = endpoint(op, extra_headers=get_headers(ctx))
    print(json.dumps(data["data"]["getAllSamples"], indent=4))


@cli.group()
def auth():
    pass


# TODO - this is just a temporary command to help us test the auth flow.
@auth.command("generate-token")
@click.argument("userid", required=True, type=int)
@click.option("--project", help="project_id:role associations to include in the header",
              type=str, default=["123:admin", "123:member", "456:member"], multiple=True)
@click.pass_context
def generate_token(ctx, userid: int, project: list[str]):
    settings = Settings()
    private_key = settings.JWK_PRIVATE_KEY

    project_dict = {}
    for item in project:
        project_id, role = item.split(":")
        if int(project_id) not in project_dict:
            project_dict[int(project_id)] = []
        project_dict[int(project_id)].append(role)
    token = create_token(private_key, userid, project_dict)
    print(token)


if __name__ == "__main__":
    cli()
