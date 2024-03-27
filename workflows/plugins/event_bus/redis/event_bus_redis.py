"""
Redis event bus plugin for local runs
"""
import json
import logging
from typing import Awaitable, Callable

from settings import RedisEventBusSettings
from plugins.plugin_types import EventBus, WorkflowStatusMessage, WorkflowFailedMessage, parse_workflow_status_message

import redis.asyncio as aioredis


class EventBusRedis(EventBus):
    def __init__(self, setings: RedisEventBusSettings) -> None:
        self._settings = setings
        self._redis = aioredis.from_url(self._settings.REDIS_URL)
        self._logger = logging.getLogger("EventBusRedis")

    async def send(self, message: WorkflowStatusMessage) -> None:
        await self._redis.lpush(self._settings.QUEUE_NAME, message.model_dump_json())  # type: ignore

    async def poll(self, handle_message: Callable[[WorkflowStatusMessage], Awaitable[None]]) -> None:
        _, message = await self._redis.brpop(self._settings.QUEUE_NAME)  # type: ignore
        try:
            await handle_message(parse_workflow_status_message(json.loads(message)))
        except Exception as e:
            self._logger.warn(f"Failed to handle message {message}: {e}")
            self._logger.exception(e)
            # there are no retries for redis messages so the workflow fails here
            await handle_message(WorkflowFailedMessage(message, str(e)))
