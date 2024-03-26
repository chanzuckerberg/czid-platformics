"""
Redis event bus plugin for local runs
"""
import json
import logging
from typing import Awaitable, Callable

from settings import RedisEventBusSettings
from plugins.plugin_types import EventBus, WorkflowStatusMessage, parse_workflow_status_message

import redis.asyncio as aioredis


class EventBusRedis(EventBus):
    def __init__(self, setings: RedisEventBusSettings) -> None:
        self._settings = setings
        self._redis = aioredis.from_url(self._settings.REDIS_URL)
        self._logger = logging.getLogger("EventBusRedis")

    async def send(self, message: WorkflowStatusMessage) -> None:
        await self._redis.lpush(self.settings.QUEUE_NAME, message.model_dump_json())  # type: ignore

    async def poll(self, handle_message: Callable[[WorkflowStatusMessage], Awaitable[None]]) -> None:
        _, message = await self._redis.brpop(self.settings.QUEUE_NAME)  # type: ignore
        for message in message:
            try:
                await handle_message(parse_workflow_status_message(json.loads(message)))
            except Exception as e:
                self._logger.warn(f"Failed to handle message {message}: {e}")
