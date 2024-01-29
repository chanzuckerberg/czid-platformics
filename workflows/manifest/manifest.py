import typing
import yaml
from abc import ABC
from collections.abc import Generator
from dataclasses import dataclass
from typing import IO, Annotated, Any, Literal, Optional

from packaging.specifiers import SpecifierSet
from pydantic import BaseModel, GetCoreSchemaHandler, ValidationError, field_validator, model_validator
from pydantic_core import InitErrorDetails, core_schema


class _SpecifierSetPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        This method defines how to parse and validate data into a SpecifierSet.
        """

        def validate_from_string(value: str) -> SpecifierSet:
            return SpecifierSet(value)

        from_string_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_string),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_string_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(SpecifierSet),
                    from_string_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda instance: str(instance)),
        )


# Annotated Type for SpecifierSet
PydanticSpecifierSet = Annotated[SpecifierSet, _SpecifierSetPydanticAnnotation]

PrimitiveTypeName = Literal["str", "int", "float", "bool"]
Primitive = str | int | float | bool


class _Input(BaseModel):
    name: str


class EntityInput(_Input):
    entity_type: str
    entity_id: str


class RawInput(_Input):
    value: typing.Any


@dataclass
class _InputValidationError(ABC):
    input_name: str
    raw_or_entity: Literal["raw", "entity"]

    def message(self) -> str:
        raise NotImplementedError


_InputValidationErrors = Generator[_InputValidationError, None, None]


@dataclass
class InputNotSupported(_InputValidationError):
    def message(self) -> str:
        return f"{self.raw_or_entity.title()} input not found: {self.input_name}"


@dataclass
class MissingRequiredInput(_InputValidationError):
    def message(self) -> str:
        return f"Missing required {self.raw_or_entity.title()} input: {self.input_name}"


@dataclass
class InputTypeInvalid(_InputValidationError):
    expected_type: str
    provided_type: str

    def message(self) -> str:
        return (
            f"Invalid type for {self.raw_or_entity} input: "
            + f"{self.input_name} (expected {self.expected_type}, got {self.provided_type})"
        )


@dataclass
class InputConstraintUnsatisfied(_InputValidationError):
    explaination: str

    def message(self) -> str:
        return f"Invalid value for {self.raw_or_entity} input: {self.input_name} ({self.explaination})"


class BaseInputArgument(BaseModel):
    name: str
    description: str
    required: bool = True


class EntityInputArgument(BaseInputArgument):
    entity_type: str

    def validate_input(self, entity_input: EntityInput) -> _InputValidationErrors:
        if entity_input.entity_type != self.entity_type:
            yield InputTypeInvalid(self.name, "entity", self.entity_type, entity_input.entity_type)


class RawInputArgument(BaseInputArgument):
    type: PrimitiveTypeName
    default: Optional[Primitive] = None
    workflow_input: Optional[str] = None
    options: list[Primitive] = []

    @model_validator(mode="after")
    def check_option_types(self):  # type: ignore
        if not self.options:
            return self

        if invalid_options := [option for option in self.options if type(option).__name__ != self.type]:
            raise ValidationError.from_exception_data(
                title=f"Invalid option type for input '{self.name}' ({self.type})",
                line_errors=[
                    InitErrorDetails(
                        type="value_error",
                        ctx={"error": ValueError(f"Invalid option type for {option} ({type(option).__name__})")},
                        input=option,
                    )
                    for option in invalid_options
                ],
            )
        return self

    @model_validator(mode="after")
    def _check_default_options(self):  # type: ignore
        if not self.options or not self.default:
            return self
        if self.default not in self.options:
            raise ValueError(f"Default value for '{self.name}': {self.default} is not in options: {self.options}")
        return self

    @model_validator(mode="after")
    def _check_default(self):  # type: ignore
        if self.default is not None and type(self.default).__name__ != self.type:
            raise ValueError(f"Default value for '{self.name}': {self.default} is not of type {self.type}")
        return self

    @model_validator(mode="after")
    def _default_not_required(self):  # type: ignore
        """
        Inputs are required by default but if a manifest has a default then it should not be required.
        This could lead to weird cases where an input is explicitly marked as required but has a default,
        which removes the required flag. This makes sense because the input is not actually required in this case.
        """
        if self.default is not None:
            self.required = False
        return self

    def validate_input(self, raw_input: RawInput) -> _InputValidationErrors:
        if self.options and raw_input.value not in self.options:
            yield InputConstraintUnsatisfied(self.name, "raw", "input not in options")
        if type(raw_input.value).__name__ != self.type:
            yield InputTypeInvalid(self.name, "raw", self.type, type(raw_input.value).__name__)


@dataclass
class InvalidInputReference:
    loader_type: Literal["input", "output"]
    loader_name: str
    loader_input_name: str
    workflow_input_name: str

    def message(self) -> str:
        path = f"{self.loader_type}_loaders.{self.loader_name}.{self.loader_input_name}"
        return f"Invalid reference at {path}:{self.workflow_input_name} (not found)"


class IOLoader(BaseModel):
    name: str
    version: PydanticSpecifierSet
    inputs: dict[str, str] = {}

    @field_validator("inputs", mode="before")
    def _inputs_default(cls, inputs_dict):  # type: ignore
        """
        Fills in default values for inputs based on the keys of the input references
        """
        # not the type we expect, return it as is to get a validation error
        if not inputs_dict or not isinstance(inputs_dict, dict):
            return inputs_dict

        return {k: v or k for k, v in inputs_dict.items()}

    def _check_references(
        self,
        loader_type: Literal["input", "output"],
        loader_name: str,
        inputs: set[str],
    ) -> typing.Generator[InvalidInputReference, None, None]:
        for k, input_name in self.inputs.items():
            if input_name not in inputs:
                yield InvalidInputReference(
                    loader_type=loader_type,
                    loader_name=loader_name,
                    loader_input_name=k,
                    workflow_input_name=input_name,
                )


class InputLoader(IOLoader):
    outputs: dict[str, str]

    @field_validator("outputs", mode="before")
    def outputs_default(cls, value):  # type: ignore
        if not value or not isinstance(value, dict):
            return value

        return {k: v or k for k, v in value.items()}


class OutputLoader(IOLoader):
    workflow_outputs: dict[str, str] = {}


class Manifest(BaseModel):
    workflow_name: str
    specification_language: typing.Literal["WDL"]
    description: str
    entity_inputs: dict[str, EntityInputArgument] = {}
    raw_inputs: dict[str, RawInputArgument] = {}
    input_loaders: list[InputLoader] = []
    output_loaders: list[OutputLoader]

    @staticmethod
    def from_yaml(manifest_yaml: str | bytes | IO[str] | IO[bytes]) -> "Manifest":
        obj = yaml.safe_load(manifest_yaml)
        return Manifest.model_validate(obj)

    @model_validator(mode="after")
    def _unique_input_names(self):  # type: ignore
        input_names = set(self.entity_inputs.keys())
        duplicate_names = [k for k in self.raw_inputs if k in input_names]
        if duplicate_names:
            raise ValueError(f"Raw input names duplicate entity input names: {duplicate_names}")
        return self

    @model_validator(mode="after")
    def _validate_references(self):  # type: ignore
        errors: list[InvalidInputReference] = []
        inputs = set(self.entity_inputs.keys()) | set(self.raw_inputs.keys())
        for input_loader in self.input_loaders:
            errors += list(input_loader._check_references("input", input_loader.name, inputs))

        for output_loader in self.output_loaders:
            errors += list(output_loader._check_references("output", output_loader.name, inputs))

        if errors:
            raise ValidationError.from_exception_data(
                title="Invalid input references",
                line_errors=[
                    InitErrorDetails(
                        type="value_error",
                        ctx={"error": ValueError(error.message())},
                        input=error.workflow_input_name,
                    )
                    for error in errors
                ],
            )
        return self

    def validate_inputs(self, entity_inputs: list[EntityInput], raw_inputs: list[RawInput]) -> _InputValidationErrors:
        for entity_or_raw, inputs, input_arguments in [
            ("entity", entity_inputs, self.entity_inputs),
            ("raw", raw_inputs, self.raw_inputs),
        ]:
            required_inputs = {k: False for k, v in input_arguments.items() if v.required}  # type: ignore
            for input in inputs:
                input_argument = input_arguments.get(input.name)  # type: ignore
                if not input_argument:
                    yield InputNotSupported(input.name, entity_or_raw)  # type: ignore
                    continue
                if input.name in required_inputs:
                    required_inputs[input.name] = True
                for error in input_argument.validate_input(input):
                    yield error
            for required_input in [k for k, v in required_inputs.items() if not v]:
                yield MissingRequiredInput(required_input, entity_or_raw)  # type: ignore


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Validate a manifest file")
    parser.add_argument("manifest", type=Path, help="Path to manifest file")
    args = parser.parse_args()
    try:
        with open(args.manifest) as f:
            Manifest.from_yaml(f)
    except ValidationError as e:
        for error in e.errors():
            path = ".".join(str(e) for e in error["loc"])
            message = error["msg"]
            if path:
                message = f"{path}: {message}"
            print(f"\033[91m{message}\033[0m")
        exit(1)
    print("\033[92mManifest is valid \u2713\033[0m")
