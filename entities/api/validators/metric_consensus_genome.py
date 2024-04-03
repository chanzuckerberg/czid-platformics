"""
Pydantic validator for MetricConsensusGenome

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class MetricConsensusGenomeCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    consensus_genome_id: Annotated[uuid.UUID, Field()]
    reference_genome_length: Annotated[float | None, Field()]
    percent_genome_called: Annotated[float | None, Field()]
    percent_identity: Annotated[float | None, Field()]
    gc_percent: Annotated[float | None, Field()]
    total_reads: Annotated[
        int | None,
        Field(
            ge=0,
            le=999999999999,
        ),
    ]
    mapped_reads: Annotated[int | None, Field()]
    ref_snps: Annotated[int | None, Field()]
    n_actg: Annotated[int | None, Field()]
    n_missing: Annotated[int | None, Field()]
    n_ambiguous: Annotated[int | None, Field()]
    coverage_depth: Annotated[float | None, Field()]
    coverage_breadth: Annotated[float | None, Field()]
    coverage_bin_size: Annotated[float | None, Field()]
    coverage_total_length: Annotated[int | None, Field()]
    coverage_viz: Annotated[list[list[float]] | None, Field()]
    producing_run_id: Annotated[uuid.UUID | None, Field()]
    collection_id: Annotated[
        int | None,
        Field(
            ge=0,
        ),
    ]
    deleted_at: Annotated[datetime.datetime | None, Field()]


class MetricConsensusGenomeUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    deleted_at: Annotated[datetime.datetime | None, Field()]
