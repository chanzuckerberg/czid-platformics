import logging
from functools import cached_property

import click
import strcase
from jinja2 import Environment, FileSystemLoader
from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition
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


class FieldWrapper:
    def __init__(self, view, wrapped_field):
        self.view = view
        self.wrapped_field = wrapped_field

    @property
    def name(self):
        return self.wrapped_field.name

    @property
    def type(self):
        return self.wrapped_field.range

    @cached_property
    def is_enum(self):
        field = self.view.get_element(self.wrapped_field.range)
        if isinstance(field, EnumDefinition):
            return True
        return False

    @cached_property
    def is_entity(self):
        field = self.view.get_element(self.wrapped_field.range)
        if isinstance(field, ClassDefinition):
            return True
        return False


class EntityWrapper:
    def __init__(self, view, wrapped_class):
        self.view = view
        self.wrapped_class = wrapped_class

    @property
    def name(self):
        return self.wrapped_class.name

    @property
    def camel_name(self):
        return self.wrapped_class.name

    @property
    def snake_name(self):
        return strcase.to_snake(self.name)

    @cached_property
    def fields(self):
        return [
            FieldWrapper(self.view, item)
            for item in self.view.class_induced_slots(self.name)
            if "Entity" not in item.domain_of
        ]

    def get_enum_fields(self):
        enumfields = self.view.all_enums()
        return (field for field in self.fields if field.range not in enumfields)

    def get_related_fields(self):
        return self.fields


def generate_db_models(environment, view):
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
        with open(dest_filename, mode="w", encoding="utf-8") as message:
            message.write(content)
            print(f"... wrote {dest_filename}")


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
    generate_db_models(environment, view)


if __name__ == "__main__":
    cli()  # type: ignore
