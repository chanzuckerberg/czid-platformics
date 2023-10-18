import json
from typing import List

from platformics.api.core.settings import RedisEventBusSettings
from plugin_types import EventBus, WorkflowStatusMessage, parse_workflow_status_message

import redis.asyncio as aioredis


class EventBusRedis(EventBus):
    def __init__(self, setings: RedisEventBusSettings) -> None:
        self.settings = setings
        self.redis = aioredis.from_url(self.settings.REDIS_URL)

    async def send(self, message: WorkflowStatusMessage) -> None:
        await self.redis.lpush(self.settings.QUEUE_NAME, json.dumps(message.asdict()))

    async def poll(self) -> List[WorkflowStatusMessage]:
        _, message = await self.redis.brpop(self.settings.QUEUE_NAME)
        return [parse_workflow_status_message(json.loads(message))]
