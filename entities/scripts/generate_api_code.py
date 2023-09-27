import logging

import click
from jinja2 import Environment, FileSystemLoader
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


def generate_enums(environment, view):
    filename = "support/enums.py"
    template = environment.get_template(f"{filename}.j2")
    logging.debug("generating enums")

    enums = []
    for enum_name in view.all_enums():
        enums.append(view.get_element(enum_name))
    content = template.render(
        enums=enums,
    )
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")


@api.command("generate")
@click.option(
    "--schemafile",
    type=str,
    required=True,
)
@click.pass_context
def api_generate(ctx: click.Context, schemafile: str) -> None:
    environment = Environment(loader=FileSystemLoader("codegen_templates/"))

    view = SchemaView(schemafile)
    view.imports_closure()

    logging.debug("generating api code")
    generate_enums(environment, view)


if __name__ == "__main__":
    cli()  # type: ignore
