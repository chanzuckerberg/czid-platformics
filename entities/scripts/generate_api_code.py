import logging

import click
from linkml_runtime.utils.schemaview import SchemaView


@click.group()
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug output",
)
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    ctx.ensure_object(dict)


@cli.group()
def api() -> None:
    pass


@api.command("generate")
@click.option(
    "--schemafile",
    type=str,
    required=True,
)
@click.pass_context
def api_generate(ctx: click.Context, schemafile: str) -> None:
    # Print the query if we're in debug mode
    logging.debug("generating api code")

    view = SchemaView(schemafile)
    view.imports_closure()
    for enum_name in view.all_enums():
        print(enum_name)
        linkml_enum = view.get_element(enum_name)
        for val in linkml_enum.permissible_values:
            print(f"  {val}")


if __name__ == "__main__":
    cli()  # type: ignore
