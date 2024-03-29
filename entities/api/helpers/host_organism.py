"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""


from typing import Any, Optional
import strawberry
import datetime
import uuid
from support.enums import HostOrganismCategory

"""
Define groupby options for HostOrganism type.
These are only used in aggregate queries.
"""


@strawberry.type
class HostOrganismGroupByOptions:
    rails_host_genome_id: Optional[int] = None
    name: Optional[str] = None
    version: Optional[str] = None
    category: Optional[HostOrganismCategory] = None
    is_deuterostome: Optional[bool] = None
    id: Optional[uuid.UUID] = None
    producing_run_id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


def build_host_organism_groupby_output(
    group_object: Optional[HostOrganismGroupByOptions],
    keys: list[str],
    value: Any,
) -> HostOrganismGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = HostOrganismGroupByOptions()

    key = keys.pop(0)
    match key:
        case _:
            pass
    setattr(group_object, key, value)
    return group_object
