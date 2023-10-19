from pydantic import BaseModel

from platformics.settings import Settings as PlatformicsSettings
from platformics.settings import APISettings as PlatformicsAPISettings
from platformics.settings import CLISettings as PlatformicCLISettings


class RedisEventBusSettings(BaseModel):
    REDIS_URL: str
    QUEUE_NAME: str


class EventBusSettings(BaseModel):
    REDIS: RedisEventBusSettings


class Settings(PlatformicsSettings):
    PLATFORMICS_WORKFLOW_RUNNER_PLUGIN: str

    PLATFORMICS_EVENT_BUS_PLUGIN: str
    PLATFORMICS_EVENT_BUS: EventBusSettings


class APISettings(PlatformicsAPISettings, Settings):
    ...


class CLISettings(PlatformicCLISettings, Settings):
    ...
