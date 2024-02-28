"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""



from typing import Any, Optional
import strawberry
import datetime
import uuid
from api.helpers.consensus_genome import ConsensusGenomeGroupByOptions, build_consensus_genome_groupby_output

"""
Define groupby options for MetricConsensusGenome type.
These are only used in aggregate queries.
"""

@strawberry.type
class MetricConsensusGenomeGroupByOptions:
    consensus_genome: Optional[ConsensusGenomeGroupByOptions] = None
    reference_genome_length: Optional[float] = None
    percent_genome_called: Optional[float] = None
    percent_identity: Optional[float] = None
    gc_percent: Optional[float] = None
    total_reads: Optional[int] = None
    mapped_reads: Optional[int] = None
    ref_snps: Optional[int] = None
    n_actg: Optional[int] = None
    n_missing: Optional[int] = None
    n_ambiguous: Optional[int] = None
    coverage_depth: Optional[float] = None
    coverage_breadth: Optional[float] = None
    coverage_bin_size: Optional[float] = None
    coverage_total_length: Optional[int] = None
    coverage_viz: Optional[list[list[float]]] = None
    id: Optional[uuid.UUID] = None
    producing_run_id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


def build_metric_consensus_genome_groupby_output(
    group_object: Optional[MetricConsensusGenomeGroupByOptions],
    keys: list[str],
    value: Any,
) -> MetricConsensusGenomeGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = MetricConsensusGenomeGroupByOptions()

    key = keys.pop(0)
    match key:
        case "consensus_genome":
            if getattr(group_object, key):
                value = build_consensus_genome_groupby_output(
                    getattr(group_object, key),
                    keys,
                    value,
                )
            else:
                value = build_consensus_genome_groupby_output(
                    None,
                    keys,
                    value,
                )
        case _:
            pass
    setattr(group_object, key, value)
    return group_object