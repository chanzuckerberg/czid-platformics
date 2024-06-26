"""
Pydantic validator for Sample

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated


class SampleCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    rails_sample_id: Annotated[int | None, Field()]
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=4,
            max_length=128,
        ),
    ]
    host_organism_id: Annotated[uuid.UUID | None, Field()]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[
        int | None,
        Field(
            ge=0,
        ),
    ]
    deleted_at: Annotated[datetime.datetime | None, Field()]


class SampleUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
            min_length=4,
            max_length=128,
        ),
    ]
    deleted_at: Annotated[datetime.datetime | None, Field()]
