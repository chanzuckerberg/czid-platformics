"""
Pydantic validator for IndexFile

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import uuid

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated


class IndexFileCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    # TODO what do we do about enums here. GraphQL is supposed to take care of that for us I think?
    #    name: Annotated[ IndexTypes, Field()]
    version: Annotated[str, StringConstraints()]
    upstream_database_id: Annotated[uuid.UUID | None, Field()]
    host_organism_id: Annotated[uuid.UUID | None, Field()]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[
        int,
        Field(
            gte=0,
        ),
    ]


class IndexFileUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    # TODO what do we do about enums here. GraphQL is supposed to take care of that for us I think?
    #    name: Annotated[ IndexTypes | None, Field()]
    version: Annotated[str | None, StringConstraints()]
