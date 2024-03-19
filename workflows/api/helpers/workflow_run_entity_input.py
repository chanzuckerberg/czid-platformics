"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""



from typing import Any, Optional
import strawberry
import datetime
import uuid
from api.helpers.workflow_run import WorkflowRunGroupByOptions, build_workflow_run_groupby_output

"""
Define groupby options for WorkflowRunEntityInput type.
These are only used in aggregate queries.
"""

@strawberry.type
class WorkflowRunEntityInputGroupByOptions:
    input_entity_id: Optional[uuid.UUID] = None
    field_name: Optional[str] = None
    entity_type: Optional[str] = None
    workflow_run: Optional[WorkflowRunGroupByOptions] = None
    id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


def build_workflow_run_entity_input_groupby_output(
    group_object: Optional[WorkflowRunEntityInputGroupByOptions],
    keys: list[str],
    value: Any,
) -> WorkflowRunEntityInputGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = WorkflowRunEntityInputGroupByOptions()

    key = keys.pop(0)
    match key:
        case "workflow_run":
            if getattr(group_object, key):
                value = build_workflow_run_groupby_output(
                    getattr(group_object, key),
                    keys,
                    value,
                )
            else:
                value = build_workflow_run_groupby_output(
                    None,
                    keys,
                    value,
                )
        case _:
            pass
    setattr(group_object, key, value)
    return group_object