"""
Pydantic validator for UpstreamDatabase

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import uuid

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class UpstreamDatabaseCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[str | None, Field()]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[int | None, Field()]


class UpstreamDatabaseUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[str | None, Field()]
