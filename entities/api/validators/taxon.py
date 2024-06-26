"""
Pydantic validator for Taxon

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


from support.enums import TaxonLevel

import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated


class TaxonCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    wikipedia_id: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    description: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    common_name: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    is_phage: Annotated[bool, Field()]
    upstream_database_id: Annotated[uuid.UUID, Field()]
    upstream_database_identifier: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    level: Annotated[TaxonLevel, Field()]
    tax_parent_id: Annotated[uuid.UUID | None, Field()]
    tax_species_id: Annotated[uuid.UUID | None, Field()]
    tax_genus_id: Annotated[uuid.UUID | None, Field()]
    tax_family_id: Annotated[uuid.UUID | None, Field()]
    tax_order_id: Annotated[uuid.UUID | None, Field()]
    tax_class_id: Annotated[uuid.UUID | None, Field()]
    tax_phylum_id: Annotated[uuid.UUID | None, Field()]
    tax_kingdom_id: Annotated[uuid.UUID | None, Field()]
    tax_superkingdom_id: Annotated[uuid.UUID | None, Field()]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[
        int | None,
        Field(
            ge=0,
        ),
    ]
    deleted_at: Annotated[datetime.datetime | None, Field()]


class TaxonUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    wikipedia_id: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    description: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    common_name: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    is_phage: Annotated[bool | None, Field()]
    level: Annotated[TaxonLevel | None, Field()]
    tax_parent_id: Annotated[uuid.UUID | None, Field()]
    tax_species_id: Annotated[uuid.UUID | None, Field()]
    tax_genus_id: Annotated[uuid.UUID | None, Field()]
    tax_family_id: Annotated[uuid.UUID | None, Field()]
    tax_order_id: Annotated[uuid.UUID | None, Field()]
    tax_class_id: Annotated[uuid.UUID | None, Field()]
    tax_phylum_id: Annotated[uuid.UUID | None, Field()]
    tax_kingdom_id: Annotated[uuid.UUID | None, Field()]
    tax_superkingdom_id: Annotated[uuid.UUID | None, Field()]
    deleted_at: Annotated[datetime.datetime | None, Field()]
