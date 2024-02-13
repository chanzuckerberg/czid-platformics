"""
Pydantic validator for Accession

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import uuid

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class AccessionCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    accession_id: Annotated[str | None, Field()]
    accession_name: Annotated[str | None, Field()]
    upstream_database_id: Annotated[uuid.UUID | None, Field()]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[int | None, Field()]


class AccessionUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    accession_name: Annotated[str | None, Field()]
