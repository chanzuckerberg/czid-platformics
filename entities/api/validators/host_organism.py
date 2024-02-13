"""
Pydantic validator for HostOrganism

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import uuid

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class HostOrganismCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[str | None, Field()]
    version: Annotated[str | None, Field()]
    # TODO what do we do about enums here. GraphQL is supposed to take care of that for us I think?
    #    category: Annotated[ HostOrganismCategory | None, Field()]
    is_deuterostome: Annotated[bool | None, Field()]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[int | None, Field()]


class HostOrganismUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[str | None, Field()]
    version: Annotated[str | None, Field()]
    # TODO what do we do about enums here. GraphQL is supposed to take care of that for us I think?
    #    category: Annotated[ HostOrganismCategory | None, Field()]
    is_deuterostome: Annotated[bool | None, Field()]
