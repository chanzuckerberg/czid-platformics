import logging
import os

import click
from jinja2 import Environment, FileSystemLoader
from linkml_runtime.utils.schemaview import SchemaView
from codegen.lib.linkml_wrappers import ViewWrapper


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


def generate_enums(output_prefix: str, environment: Environment, view: ViewWrapper) -> None:
    filename = "support/enums.py"
    template = environment.get_template(f"{filename}.j2")
    logging.debug("generating enums")

    content = template.render(
        enums=view.enums,
    )
    with open(os.path.join(output_prefix, filename), mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")


def generate_entity_subclass_files(
    output_prefix: str, template_filename: str, environment: Environment, view: ViewWrapper
) -> None:
    template = environment.get_template(f"{template_filename}.j2")
    logging.debug("generating enums")

    for entity in view.entities:
        content = template.render(
            cls=entity,
            view=view,
        )
        dest_filename = str(template_filename).replace("class_name", entity.snake_name)
        with open(os.path.join(output_prefix, dest_filename), mode="w", encoding="utf-8") as outfile:
            outfile.write(content)
            print(f"... wrote {dest_filename}")


def generate_entity_import_files(output_prefix: str, environment: Environment, view: ViewWrapper) -> None:
    import_templates = ["database/models/__init__.py", "api/queries.py"]
    classes = view.entities
    for filename in import_templates:
        import_template = environment.get_template(f"{filename}.j2")
        content = import_template.render(
            classes=classes,
            view=view,
        )
        with open(os.path.join(output_prefix, filename), mode="w", encoding="utf-8") as outfile:
            outfile.write(content)
            print(f"... wrote {filename}")


def generate_gql_type_files(
    output_prefix: str, template_filename: str, environment: Environment, view: ViewWrapper
) -> None:
    template = environment.get_template(f"{template_filename}.j2")
    logging.debug("generating gql types")

    for entity in view.entities:
        content = template.render(
            cls=entity,
            view=view,
        )
        dest_filename = str(template_filename).replace("class_name", (entity.snake_name))
        with open(os.path.join(output_prefix, dest_filename), mode="w", encoding="utf-8") as outfile:
            outfile.write(content)
            print(f"... wrote {dest_filename}")


def generate_cerbos_policies(output_prefix: str, environment: Environment, view: ViewWrapper) -> None:
    filename = "cerbos/policies/class_name.yaml"
    generate_entity_subclass_files(output_prefix, filename, environment, view)


def generate_db_models(output_prefix: str, environment: Environment, view: ViewWrapper) -> None:
    filename = "database/models/class_name.py"
    generate_entity_subclass_files(output_prefix, filename, environment, view)


def generate_gql_types(output_prefix: str, environment: Environment, view: ViewWrapper) -> None:
    filename = "api/types/class_name.py"
    generate_gql_type_files(output_prefix, filename, environment, view)


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
    wrapped_view = ViewWrapper(view)

    logging.debug("generating api code")
    generate_enums(output_prefix, environment, wrapped_view)
    generate_db_models(output_prefix, environment, wrapped_view)
    generate_cerbos_policies(output_prefix, environment, wrapped_view)
    generate_entity_import_files(output_prefix, environment, wrapped_view)
    generate_gql_types(output_prefix, environment, wrapped_view)


if __name__ == "__main__":
    cli()  # type: ignore
