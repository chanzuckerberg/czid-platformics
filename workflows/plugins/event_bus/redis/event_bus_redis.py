import json
import os
from typing import List

from plugin_types import EventBus, WorkflowStatusMessage, parse_workflow_status_message

import redis.asyncio as aioredis

REDIS_URL = os.environ.get('CZID__EVENT_BUS_REDIS__REDIS_URL', 'redis://localhost')
QUEUE_NAME = os.environ.get('CZID__EVENT_BUS_REDIS__QUEUE_NAME', 'workflow_status')

class EventBusRedis(EventBus):
    def __init__(self):
        self.redis = aioredis.from_url(REDIS_URL)


    async def send(self, message: WorkflowStatusMessage):
        await self.redis.lpush(QUEUE_NAME, json.dumps(message.asdict()))

    async def poll(self) -> List[WorkflowStatusMessage]:
        _, message = await self.redis.brpop(QUEUE_NAME)
        return [parse_workflow_status_message(json.loads(message))]

