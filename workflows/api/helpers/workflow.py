"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""


from typing import Any, Optional
import strawberry
import datetime
import uuid

"""
Define groupby options for Workflow type.
These are only used in aggregate queries.
"""


@strawberry.type
class WorkflowGroupByOptions:
    name: Optional[str] = None
    default_version: Optional[str] = None
    minimum_supported_version: Optional[str] = None
    id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


def build_workflow_groupby_output(
    group_object: Optional[WorkflowGroupByOptions],
    keys: list[str],
    value: Any,
) -> WorkflowGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = WorkflowGroupByOptions()

    key = keys.pop(0)
    match key:
        case _:
            pass
    setattr(group_object, key, value)
    return group_object
