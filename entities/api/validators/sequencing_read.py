"""
Pydantic validator for SequencingRead

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


from support.enums import SequencingProtocol, SequencingTechnology, NucleicAcid

import uuid

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated


class SequencingReadCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    sample_id: Annotated[uuid.UUID | None, Field()]
    protocol: Annotated[SequencingProtocol | None, Field()]
    technology: Annotated[SequencingTechnology, Field()]
    nucleic_acid: Annotated[NucleicAcid, Field()]
    clearlabs_export: Annotated[bool, Field()]
    medaka_model: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    taxon_id: Annotated[uuid.UUID | None, Field()]
    primer_file_id: Annotated[uuid.UUID | None, Field()]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]


class SequencingReadUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    nucleic_acid: Annotated[NucleicAcid | None, Field()]
    clearlabs_export: Annotated[bool | None, Field()]
    medaka_model: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
