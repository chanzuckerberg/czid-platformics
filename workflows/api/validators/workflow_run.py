"""
Pydantic validator for WorkflowRun

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long




import typing
import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated





class WorkflowRunCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)

    collection_id: Annotated[ int, Field()]
    started_at: Annotated[ datetime.datetime | None, Field()]
    ended_at: Annotated[ datetime.datetime | None, Field()]
    execution_id: Annotated[ str | None, Field()]
    outputs_json: Annotated[ str | None, Field()]
    workflow_runner_inputs_json: Annotated[ str | None, Field()]
# TODO what do we do about enums here. GraphQL is supposed to take care of that for us I think?
#    status: Annotated[ WorkflowRunStatus | None, Field()] 
    workflow_version_id: Annotated[ uuid.UUID | None, Field()]
    raw_inputs_json: Annotated[ str | None, Field()] 
class WorkflowRunUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)

    collection_id: Annotated[ int | None, Field()]
    started_at: Annotated[ datetime.datetime | None, Field()]
    ended_at: Annotated[ datetime.datetime | None, Field()]
    execution_id: Annotated[ str | None, Field()]
    outputs_json: Annotated[ str | None, Field()]
    workflow_runner_inputs_json: Annotated[ str | None, Field()]
# TODO what do we do about enums here. GraphQL is supposed to take care of that for us I think?
#    status: Annotated[ WorkflowRunStatus | None, Field()] 
    workflow_version_id: Annotated[ uuid.UUID | None, Field()]
    raw_inputs_json: Annotated[ str | None, Field()] 