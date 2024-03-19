"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""


from typing import Any, Optional
import strawberry
import datetime
import uuid
from api.helpers.taxon import TaxonGroupByOptions, build_taxon_groupby_output
from api.helpers.sequencing_read import SequencingReadGroupByOptions, build_sequencing_read_groupby_output
from api.helpers.reference_genome import ReferenceGenomeGroupByOptions, build_reference_genome_groupby_output
from api.helpers.accession import AccessionGroupByOptions, build_accession_groupby_output

"""
Define groupby options for ConsensusGenome type.
These are only used in aggregate queries.
"""


@strawberry.type
class ConsensusGenomeGroupByOptions:
    taxon: Optional[TaxonGroupByOptions] = None
    sequencing_read: Optional[SequencingReadGroupByOptions] = None
    reference_genome: Optional[ReferenceGenomeGroupByOptions] = None
    accession: Optional[AccessionGroupByOptions] = None
    id: Optional[uuid.UUID] = None
    producing_run_id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


def build_consensus_genome_groupby_output(
    group_object: Optional[ConsensusGenomeGroupByOptions],
    keys: list[str],
    value: Any,
) -> ConsensusGenomeGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = ConsensusGenomeGroupByOptions()

    key = keys.pop(0)
    match key:
        case "taxon":
            if getattr(group_object, key):
                value = build_taxon_groupby_output(
                    getattr(group_object, key),
                    keys,
                    value,
                )
            else:
                value = build_taxon_groupby_output(
                    None,
                    keys,
                    value,
                )
        case "sequencing_read":
            if getattr(group_object, key):
                value = build_sequencing_read_groupby_output(
                    getattr(group_object, key),
                    keys,
                    value,
                )
            else:
                value = build_sequencing_read_groupby_output(
                    None,
                    keys,
                    value,
                )
        case "reference_genome":
            if getattr(group_object, key):
                value = build_reference_genome_groupby_output(
                    getattr(group_object, key),
                    keys,
                    value,
                )
            else:
                value = build_reference_genome_groupby_output(
                    None,
                    keys,
                    value,
                )
        case "accession":
            if getattr(group_object, key):
                value = build_accession_groupby_output(
                    getattr(group_object, key),
                    keys,
                    value,
                )
            else:
                value = build_accession_groupby_output(
                    None,
                    keys,
                    value,
                )
        case _:
            pass
    setattr(group_object, key, value)
    return group_object
