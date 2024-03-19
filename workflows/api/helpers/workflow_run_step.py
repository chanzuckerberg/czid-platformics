"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""



from typing import Any, Optional
import strawberry
import datetime
import uuid
from support.enums import WorkflowRunStepStatus
from api.helpers.workflow_run import WorkflowRunGroupByOptions, build_workflow_run_groupby_output

"""
Define groupby options for WorkflowRunStep type.
These are only used in aggregate queries.
"""

@strawberry.type
class WorkflowRunStepGroupByOptions:
    workflow_run: Optional[WorkflowRunGroupByOptions] = None
    started_at: Optional[datetime.datetime] = None
    ended_at: Optional[datetime.datetime] = None
    status: Optional[WorkflowRunStepStatus] = None
    id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


def build_workflow_run_step_groupby_output(
    group_object: Optional[WorkflowRunStepGroupByOptions],
    keys: list[str],
    value: Any,
) -> WorkflowRunStepGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = WorkflowRunStepGroupByOptions()

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