"""
Pydantic validator for ConsensusGenome

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import uuid

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class ConsensusGenomeCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    taxon_id: Annotated[uuid.UUID, Field()]
    sequence_read_id: Annotated[uuid.UUID, Field()]
    reference_genome_id: Annotated[uuid.UUID | None, Field()]
    accession_id: Annotated[uuid.UUID | None, Field()]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]