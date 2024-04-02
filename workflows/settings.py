"""
A module that contains settings to load into the web app
"""

from typing import Optional
from pydantic import BaseModel

from platformics.settings import Settings as PlatformicsSettings
from platformics.settings import APISettings as PlatformicsAPISettings
from platformics.settings import CLISettings as PlatformicCLISettings


class SWIPEEventBusSettings(BaseModel):
    SQS_QUEUE_URL: str
    SQS_ENDPOINT: Optional[str] = None
    SFN_ENDPOINT: Optional[str] = None


class RedisEventBusSettings(BaseModel):
    REDIS_URL: str
    QUEUE_NAME: str


class EventBusSettings(BaseModel):
    REDIS: RedisEventBusSettings
    SWIPE: SWIPEEventBusSettings


class LocalWorkflowRunnerSettings(BaseModel):
    S3_ENDPOINT: Optional[str] = None


class SWIPEWorkflowRunnerSettings(BaseModel):
    STATE_MACHINE_ARN: str
    OUTPUT_S3_PREFIX: str
    SFN_ENDPOINT: Optional[str] = None


class WorkflowRunnerSettings(BaseModel):
    LOCAL: LocalWorkflowRunnerSettings
    SWIPE: SWIPEWorkflowRunnerSettings


class Settings(PlatformicsSettings):
    PLATFORMICS_WORKFLOW_RUNNER_PLUGIN: str
    PLATFORMICS_WORKFLOW_RUNNER: WorkflowRunnerSettings

    PLATFORMICS_EVENT_BUS_PLUGIN: str
    PLATFORMICS_EVENT_BUS: EventBusSettings


class APISettings(PlatformicsAPISettings, Settings): ...


class CLISettings(PlatformicCLISettings, Settings): ...
