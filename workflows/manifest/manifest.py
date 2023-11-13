import json
import semver
import typing
from pathlib import Path
from database.models.workflow import Workflow, WorkflowVersion
from sqlalchemy.orm import Session
from pydantic import BaseModel, model_validator


class PydanticVersion(semver.Version):
    @classmethod
    def _parse(cls, version: str, *args: typing.Any) -> semver.Version:
        return cls.parse(version)

    @classmethod
    def __get_validators__(cls):  # type: ignore
        """Return a list of validator methods for pydantic models."""
        yield cls._parse


def convert_semver(v: PydanticVersion) -> str:
    return str(v)


class ManifestModel(BaseModel):
    class Config:
        json_encoders = {PydanticVersion: convert_semver}


class EntityInput(ManifestModel):
    name: str
    description: str
    entity_type: str
    required: bool = False


class RawInput(ManifestModel):
    name: str
    description: str
    default: typing.Optional[typing.Any]
    required: bool = False
    opions: list[str] = []
    kind: typing.Literal["string", "int", "float", "boolean", "enum"]

    @model_validator(mode="after")
    def check_options(self):
        if self.kind == "enum" and not self.opions:
            raise ValueError("Must specify options for enum")
        if self.default is not None and self.default not in self.opions:
            raise ValueError("Default must be one of options")
        return self


class InputReference(ManifestModel):
    entity_input: typing.Optional[str]
    raw_input: typing.Optional[str]
    _loader_input: typing.Optional[str]

    @property
    def loader_input(self) -> str:
        if self._loader_input:
            return self._loader_input
        if self.entity_input is not None:
            return self.entity_input
        if self.raw_input is not None:
            return self.raw_input
        raise ValueError("No input specified")

    @model_validator(mode="after")
    def check_at_least_one(self):
        if not (self.entity_input or self.raw_input):
            raise ValueError("Must specify at least one of entity_input or raw_input")
        return self


class InputLoaderOutputLink(BaseModel):
    loader_output: str
    _workflow_input: typing.Optional[str]

    @property
    def workflow_input(self) -> str:
        if self._workflow_input:
            return self._workflow_input
        return self.loader_output


class InputLoader(ManifestModel):
    name: str
    version: PydanticVersion
    workflow_input: str
    inputs: list[InputReference]
    outputs: list[InputLoaderOutputLink]


class EntityOutput(ManifestModel):
    name: str
    entity_type: str
    version: PydanticVersion


class WorkflowOutput(ManifestModel):
    name: str
    workflow_data_type: str
    description: str


class OutputFieldMap(ManifestModel):
    name: str
    reference: str


class OutputLoader(ManifestModel):
    name: str
    version: PydanticVersion
    entity_output: str
    fields: list[OutputFieldMap]


class Manifest(ManifestModel):
    workflow_name: str
    workflow_version: PydanticVersion
    type: typing.Literal["WDL"]
    description: str
    package_uri: str
    entity_inputs: dict[str, EntityInput]
    raw_inputs: dict[str, RawInput]
    input_loaders: list[InputLoader]
    entity_outputs: dict[str, EntityOutput]
    output_loaders: list[OutputLoader]


def load_manifest(manifest_json: str) -> Manifest:
    manifest_dict = json.loads(manifest_json)
    manifest = Manifest.model_validate(manifest_dict)
    return manifest


def import_manifests(session: Session) -> None:
    manifests_dir = Path("/workflows/manifests/")

    for manifest_file in manifests_dir.glob("*.json"):
        with open(manifest_file) as manifest_f:
            manifest_str = manifest_f.read()
            manifest = load_manifest(manifest_str)

        workflow = (
            session.query(Workflow)
            .filter(Workflow.name == manifest.name, Workflow.default_version == str(manifest.version))
            .first()
        )

        if workflow is None:
            workflow = Workflow(
                name=manifest.name,
                default_version=str(manifest.version),
                minimum_supported_version=str(manifest.version),
            )
            session.add(workflow)
            session.commit()

        workflow_version = WorkflowVersion(graph_json="{}", workflow=workflow, manifest=manifest_str)  # TODO: fill in
        session.add(workflow_version)
        session.commit()
