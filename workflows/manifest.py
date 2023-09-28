import json
from pydantic import BaseModel
import semver


class PydanticVersion(semver.Version):
    @classmethod
    def _parse(cls, version, *args):
        return cls.parse(version)

    @classmethod
    def __get_validators__(cls):
        """Return a list of validator methods for pydantic models."""
        yield cls._parse


def convert_semver(v: PydanticVersion):
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
