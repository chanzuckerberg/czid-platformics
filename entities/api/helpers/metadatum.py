"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""



from typing import Any, Optional
import strawberry
import datetime
import uuid
from api.helpers.sample import SampleGroupByOptions, build_sample_groupby_output

"""
Define groupby options for Metadatum type.
These are only used in aggregate queries.
"""

@strawberry.type
class MetadatumGroupByOptions:
    sample: Optional[SampleGroupByOptions] = None
    field_name: Optional[str] = None
    value: Optional[str] = None
    id: Optional[uuid.UUID] = None
    producing_run_id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


def build_metadatum_groupby_output(
    group_object: Optional[MetadatumGroupByOptions],
    keys: list[str],
    value: Any,
) -> MetadatumGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = MetadatumGroupByOptions()

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
        case _:
            if key not in group_object.__annotations__:
                raise Exception(f"Unknown groupby key: {key}")
    setattr(group_object, key, value)
    return group_object