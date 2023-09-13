from typing import Dict, List, Literal, Optional
from semver import Version
from dataclasses import asdict, dataclass, field

from entity_interface import Entity

WorkflowDataType = str
EntityType = str

@dataclass
class EntityTypeConstraint:
    entity_type: EntityType
    description: Optional[str] = None
    min_version: Optional[Version] = None
    max_version: Optional[Version] = None
    # TODO: add metadata

    def to_dict(self):
        _dict = asdict(self)
        if _dict["min_version"]:
            _dict["min_version"] = str(_dict["min_version"])
        if _dict["max_version"]:
            _dict["max_version"] = str(_dict["max_version"])
        return _dict

    def satisfies(self, entity: Entity) -> bool:
        if entity.entity_type != self.entity_type:
            return False
        if entity.version is None:
            return True
        if self.min_version is not None and entity.version < self.min_version:
            return False
        if self.max_version is not None and entity.version > self.max_version:
            return False
        return True

@dataclass
class WorkflowTypeAnnotation:
    name: str
    version: Version
    metadata: Dict[str, str] = field(default_factory=dict)

@dataclass
class WorkflowData:
    workflow_data_type: WorkflowDataType
    description: Optional[str] = None
    version: Version = field(default_factory=lambda: Version(0))
    type_annotation: Optional[WorkflowTypeAnnotation] = None

    def to_dict(self):
        _dict = asdict(self)
        _dict["version"] = str(_dict["version"])
        return _dict

@dataclass
class WorkflowInput:
    data: WorkflowData
    required: bool = False

@dataclass
class InputLoader:
    name: str
    version: Version
    workflow_input: WorkflowInput
    entity_inputs: Dict[str, EntityTypeConstraint] = field(default_factory=dict)

    def to_dict(self):
        _dict = asdict(self)
        _dict["version"] = str(_dict["version"])
        return _dict

@dataclass
class EntityOutput:
    entity_type: EntityType
    version: Version = field(default_factory=lambda: Version(0))

@dataclass
class WorkflowOutput(WorkflowData):
    pass

@dataclass
class OutputLoader:
    name: str
    version: Version
    entity_output: EntityOutput
    workflow_outputs: Dict[str, WorkflowOutput] = field(default_factory=dict)

    def to_dict(self):
        _dict = asdict(self)
        _dict["version"] = str(_dict["version"])
        return _dict

@dataclass
class WorkflowVersion:
    name: str
    version: Version
    type: Literal["WDL"]
    deprecated: bool
    description: str
    entity_inputs: Dict[str, EntityTypeConstraint] = field(default_factory=dict)
    workflow_inputs: Dict[str, WorkflowInput] = field(default_factory=dict)
    input_loaders: List[InputLoader] = field(default_factory=list)
    workflow_outputs: Dict[str, WorkflowOutput] = field(default_factory=dict)
    entity_outputs: Dict[str, EntityOutput] = field(default_factory=dict)
    output_loaders: List[OutputLoader] = field(default_factory=list)

fasta_entity = EntityTypeConstraint(
    entity_type="fasta",
    description="A fasta file",
)

fasta_workflow_input = WorkflowInput(
    data=WorkflowData(
        workflow_data_type="File",
        description="A fasta file",
        version=Version(1, 0, 0),
        type_annotation=WorkflowTypeAnnotation(
            name="fasta",
            version=Version(1, 0, 0),
        ),
    ),
    required=True,
)

sequence_id_workflow_output = WorkflowOutput(
    workflow_data_type="String",
    description="The id of the first sequence",
)

sequence_workflow_output = WorkflowOutput(
    workflow_data_type="String",
    description="The first sequence",
)

sequence_entity_output = EntityOutput(
    entity_type="Sequence",
    version=Version(1, 0, 0),
)

first_sequence = WorkflowVersion(
    name="first_sequence",
    version=Version(1, 0, 0),
    type="WDL",
    deprecated=False,
    description="A workflow that takes a sequence and returns the first base",
    entity_inputs={
        "fasta": fasta_entity,
    },
    workflow_inputs={
        "sequences": fasta_workflow_input,
    },
    input_loaders=[
        InputLoader(
            name="fasta",
            version=Version(1, 0, 0),
            workflow_input=fasta_workflow_input,
            entity_inputs={
                "fasta": fasta_entity,
            },
        ),
    ],
    workflow_outputs={
        "id": sequence_id_workflow_output,
        "sequence": sequence_workflow_output,
    },
    entity_outputs={
        "sequence": sequence_entity_output,
    },
    output_loaders=[
        OutputLoader(
            name="sequence",
            version=Version(1, 0, 0),
            entity_output=sequence_entity_output,
            workflow_outputs={
                "id": sequence_id_workflow_output,
                "sequence": sequence_workflow_output,
            },
        ),
    ],
)

name_workflow_output = WorkflowOutput(
    workflow_data_type="String",
    description="The name of the sample",
)

location_workflow_output = WorkflowOutput(
    workflow_data_type="String",
    description="The location of the sample",
)

sample_entity_output = EntityOutput(
    entity_type="sample",
    version=Version(0, 0, 0),
)

static_sample = WorkflowVersion(
    name="first_sequence",
    version=Version(1, 0, 0),
    type="WDL",
    deprecated=False,
    description="A workflow that takes a sequence and returns the first base",
    entity_inputs={},
    workflow_inputs={},
    input_loaders=[],
    workflow_outputs={
        "name": name_workflow_output,
        "location": location_workflow_output,
    },
    entity_outputs={
        "sample": sample_entity_output,
    },
    output_loaders=[
        OutputLoader(
            name="sample",
            version=Version(1, 0, 0),
            entity_output=sample_entity_output,
            workflow_outputs={
                "name": name_workflow_output,
                "location": location_workflow_output,
            },
        )
    ],
)