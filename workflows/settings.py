"""
A module that contains settings to load into the web app
"""

from pydantic import BaseModel

from platformics.settings import Settings as PlatformicsSettings
from platformics.settings import APISettings as PlatformicsAPISettings
from platformics.settings import CLISettings as PlatformicCLISettings


class SWIPEEventBusSettings(BaseModel):
    SQS_QUEUE_URL: str
    BOTO_ENDPOINT_URL: str


class RedisEventBusSettings(BaseModel):
    REDIS_URL: str
    QUEUE_NAME: str


class EventBusSettings(BaseModel):
    REDIS: RedisEventBusSettings
    SWIPE: SWIPEEventBusSettings


class Settings(PlatformicsSettings):
    PLATFORMICS_WORKFLOW_RUNNER_PLUGIN: str

    PLATFORMICS_EVENT_BUS_PLUGIN: str
    PLATFORMICS_EVENT_BUS: EventBusSettings


class APISettings(PlatformicsAPISettings, Settings):
    ...


class CLISettings(PlatformicCLISettings, Settings):
    ...
