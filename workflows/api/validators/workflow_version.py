"""
Pydantic validator for WorkflowVersion

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import uuid

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated


class WorkflowVersionCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    graph_json: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    workflow_uri: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    version: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    manifest: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    workflow_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]