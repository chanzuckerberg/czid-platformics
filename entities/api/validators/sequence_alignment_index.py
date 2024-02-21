"""
Pydantic validator for SequenceAlignmentIndex

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import uuid

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class SequenceAlignmentIndexCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)

    collection_id: Annotated[int, Field()]
    index_file_id: Annotated[uuid.UUID | None, Field()]
    reference_genome_id: Annotated[uuid.UUID | None, Field()]
    # TODO what do we do about enums here. GraphQL is supposed to take care of that for us I think?
    #    tool: Annotated[ AlignmentTool, Field()]
    version: Annotated[str | None, Field()]


class SequenceAlignmentIndexUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)

    collection_id: Annotated[int | None, Field()]
    index_file_id: Annotated[uuid.UUID | None, Field()]
    reference_genome_id: Annotated[uuid.UUID | None, Field()]
    # TODO what do we do about enums here. GraphQL is supposed to take care of that for us I think?
    #    tool: Annotated[ AlignmentTool | None, Field()]
    version: Annotated[str | None, Field()]
