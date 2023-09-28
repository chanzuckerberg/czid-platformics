import logging
import os

import click
import strcase
from jinja2 import Environment, FileSystemLoader
from linkml_runtime.utils.schemaview import SchemaView
from codegen.lib.linkml_wrappers import EntityWrapper


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


def generate_enums(output_prefix: str, environment: Environment, view: SchemaView) -> None:
    filename = "support/enums.py"
    template = environment.get_template(f"{filename}.j2")
    logging.debug("generating enums")

    enums = []
    for enum_name in view.all_enums():
        enums.append(view.get_element(enum_name))
    content = template.render(
        enums=enums,
    )
    with open(os.path.join(output_prefix, filename), mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")


def generate_db_models(output_prefix: str, environment: Environment, view: SchemaView) -> None:
    filename = "database/models/class_name.py"
    template = environment.get_template(f"{filename}.j2")
    logging.debug("generating enums")

    for class_name in view.all_classes():
        cls = view.get_element(class_name)
        # If this class doesn't descend from Entity, skip it.
        if cls.is_a != "Entity":
            continue
        wrapped = EntityWrapper(view, cls)
        content = template.render(
            cls=wrapped,
            view=view,
        )
        dest_filename = str(filename).replace("class_name", strcase.to_snake(class_name))
        with open(os.path.join(output_prefix, dest_filename), mode="w", encoding="utf-8") as message:
            message.write(content)
            print(f"... wrote {dest_filename}")

def generate_cerbos_policies(output_prefix: str, environment: Environment, view: SchemaView) -> None:
    filename = "cerbos/policies/class_name.yaml"
    template = environment.get_template(f"{filename}.j2")
    logging.debug("generating enums")

    for class_name in view.all_classes():
        cls = view.get_element(class_name)
        # If this class doesn't descend from Entity, skip it.
        if cls.is_a != "Entity":
            continue
        wrapped = EntityWrapper(view, cls)
        content = template.render(
            cls=wrapped,
            view=view,
        )
        dest_filename = str(filename).replace("class_name", strcase.to_snake(class_name))
        with open(os.path.join(output_prefix, dest_filename), mode="w", encoding="utf-8") as message:
            message.write(content)
            print(f"... wrote {dest_filename}")


@api.command("generate")
@click.option(
    "--schemafile",
    type=str,
    required=True,
)
@click.option(
    "--output-prefix",
    type=str,
    required=True,
)
@click.pass_context
def api_generate(ctx: click.Context, schemafile: str, output_prefix: str) -> None:
    environment = Environment(loader=FileSystemLoader("codegen/templates/"))

    view = SchemaView(schemafile)
    view.imports_closure()

    logging.debug("generating api code")
    generate_enums(output_prefix, environment, view)
    generate_db_models(output_prefix, environment, view)
    generate_cerbos_policies(output_prefix, environment, view)


if __name__ == "__main__":
    cli()  # type: ignore
