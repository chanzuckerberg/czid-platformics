"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""

from typing import Any, Optional
import strawberry
import datetime
import uuid
from api.helpers.upstream_database import UpstreamDatabaseGroupByOptions, build_upstream_database_groupby_output

"""
Define groupby options for Accession type.
These are only used in aggregate queries.
"""


@strawberry.type
class AccessionGroupByOptions:
    accession_id: Optional[str] = None
    accession_name: Optional[str] = None
    upstream_database: Optional[UpstreamDatabaseGroupByOptions] = None
    id: Optional[uuid.UUID] = None
    producing_run_id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


def build_accession_groupby_output(
    group_object: Optional[AccessionGroupByOptions],
    keys: list[str],
    value: Any,
) -> AccessionGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = AccessionGroupByOptions()

    key = keys.pop(0)
    match key:
        case "upstream_database":
            if getattr(group_object, key):
                value = build_upstream_database_groupby_output(
                    getattr(group_object, key),
                    keys,
                    value,
                )
            else:
                value = build_upstream_database_groupby_output(
                    None,
                    keys,
                    value,
                )
        case _:
            pass
    setattr(group_object, key, value)
    return group_object
