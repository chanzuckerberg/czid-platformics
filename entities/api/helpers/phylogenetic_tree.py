"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""


from typing import Any, Optional
import strawberry
import datetime
import uuid
from support.enums import PhylogeneticTreeFormat


@strawberry.type
class PhylogeneticTreeGroupByOptions:
    format: Optional[PhylogeneticTreeFormat] = None
    id: Optional[uuid.UUID] = None
    producing_run_id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


def build_phylogenetic_tree_groupby_output(
    group_object: Optional[PhylogeneticTreeGroupByOptions],
    keys: list[str],
    value: Any,
) -> PhylogeneticTreeGroupByOptions:
    if not group_object:
        group_object = PhylogeneticTreeGroupByOptions()

    key = keys.pop(0)
    match key:
        case _:
            pass  # TODO: log warning/error if key is not recognized
    setattr(group_object, key, value)
    return group_object
