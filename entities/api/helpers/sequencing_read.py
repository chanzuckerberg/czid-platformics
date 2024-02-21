"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""



from typing import Any, Optional
import strawberry
import datetime
import uuid
from support.enums import SequencingProtocol, SequencingTechnology, NucleicAcid
from api.helpers.sample import SampleGroupByOptions, build_sample_groupby_output
from api.helpers.taxon import TaxonGroupByOptions, build_taxon_groupby_output
from api.helpers.genomic_range import GenomicRangeGroupByOptions, build_genomic_range_groupby_output

"""
Define groupby options for SequencingRead type.
These are only used in aggregate queries.
"""

@strawberry.type
class SequencingReadGroupByOptions:
    sample: Optional[SampleGroupByOptions] = None
    protocol: Optional[SequencingProtocol] = None
    technology: Optional[SequencingTechnology] = None
    nucleic_acid: Optional[NucleicAcid] = None
    clearlabs_export: Optional[bool] = None
    medaka_model: Optional[str] = None
    taxon: Optional[TaxonGroupByOptions] = None
    primer_file: Optional[GenomicRangeGroupByOptions] = None
    id: Optional[uuid.UUID] = None
    producing_run_id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


def build_sequencing_read_groupby_output(
    group_object: Optional[SequencingReadGroupByOptions],
    keys: list[str],
    value: Any,
) -> SequencingReadGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = SequencingReadGroupByOptions()

    key = keys.pop(0)
    match key:
        case "sample":
            if getattr(group_object, key):
                value = build_sample_groupby_output(
                    getattr(group_object, key),
                    keys,
                    value,
                )
            else:
                value = build_sample_groupby_output(
                    None,
                    keys,
                    value,
                )
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
        case "genomic_range":
            if getattr(group_object, key):
                value = build_genomic_range_groupby_output(
                    getattr(group_object, key),
                    keys,
                    value,
                )
            else:
                value = build_genomic_range_groupby_output(
                    None,
                    keys,
                    value,
                )
        case _:
            pass
    setattr(group_object, key, value)
    return group_object