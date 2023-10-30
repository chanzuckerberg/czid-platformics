import json
import semver
import typing
from pathlib import Path
from database.models.workflow import Workflow, WorkflowVersion
from sqlalchemy.orm import Session
from pydantic import BaseModel


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


class WorkflowTypeAnnotation(ManifestModel):
    name: str
    version: PydanticVersion


class WorkflowInput(ManifestModel):
    name: str
    workflow_data_type: str
    description: str
    version: PydanticVersion
    type_annotations: list[WorkflowTypeAnnotation]


class EntityInput(ManifestModel):
    name: str
    entity_type: str
    description: str


class EntityInputReference(ManifestModel):
    name: str
    value: str


class InputLoader(ManifestModel):
    name: str
    version: PydanticVersion
    workflow_input: str
    entity_inputs: list[EntityInputReference]


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
    name: str
    version: PydanticVersion
    type: str = "WDL"
    deprecated: bool = False
    description: str
    package_uri: str
    entity_inputs: list[EntityInput]
    workflow_inputs: list[WorkflowInput]
    input_loaders: list[InputLoader]
    workflow_outputs: list[WorkflowOutput]
    entity_outputs: list[EntityOutput]
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
