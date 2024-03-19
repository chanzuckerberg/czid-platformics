"""
Pydantic validator for Metadatum

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated


class MetadatumCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    sample_id: Annotated[uuid.UUID, Field()]
    field_name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    value: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]
    deleted_at: Annotated[datetime.datetime | None, Field()]


class MetadatumUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    value: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    deleted_at: Annotated[datetime.datetime | None, Field()]
