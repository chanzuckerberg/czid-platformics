"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""


from typing import Any, Optional
import strawberry
import datetime
import uuid
from support.enums import WorkflowRunStatus
from api.helpers.workflow_version import WorkflowVersionGroupByOptions, build_workflow_version_groupby_output

"""
Define groupby options for WorkflowRun type.
These are only used in aggregate queries.
"""


@strawberry.type
class WorkflowRunGroupByOptions:
    rails_workflow_run_id: Optional[int] = None
    started_at: Optional[datetime.datetime] = None
    ended_at: Optional[datetime.datetime] = None
    execution_id: Optional[str] = None
    outputs_json: Optional[str] = None
    workflow_runner_inputs_json: Optional[str] = None
    status: Optional[WorkflowRunStatus] = None
    error_label: Optional[str] = None
    error_message: Optional[str] = None
    workflow_version: Optional[WorkflowVersionGroupByOptions] = None
    raw_inputs_json: Optional[str] = None
    deprecated_by: Optional["WorkflowRunGroupByOptions"] = None
    id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


def build_workflow_run_groupby_output(
    group_object: Optional[WorkflowRunGroupByOptions],
    keys: list[str],
    value: Any,
) -> WorkflowRunGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = WorkflowRunGroupByOptions()

    key = keys.pop(0)
    match key:
        case "workflow_version":
            if getattr(group_object, key):
                value = build_workflow_version_groupby_output(
                    getattr(group_object, key),
                    keys,
                    value,
                )
            else:
                value = build_workflow_version_groupby_output(
                    None,
                    keys,
                    value,
                )
        case _:
            pass
    setattr(group_object, key, value)
    return group_object
