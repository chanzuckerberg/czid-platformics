"""
Pydantic validator for PhylogeneticTree

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


from support.enums import PhylogeneticTreeFormat

import uuid

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class PhylogeneticTreeCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    format: Annotated[PhylogeneticTreeFormat, Field()]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]


class PhylogeneticTreeUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    format: Annotated[PhylogeneticTreeFormat | None, Field()]
