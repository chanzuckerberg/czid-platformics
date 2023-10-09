from typing import List
from threading import RLock
from plugin_types import EventBus, WorkflowStatusMessage


# TODO: don't lock
class EventBusLocal(EventBus):
    def __init__(self) -> None:
        self._queue: List[WorkflowStatusMessage] = []
        self._lock = RLock()

    async def send(self, message: WorkflowStatusMessage) -> None:
        with self._lock:
            self._queue.append(message)

    async def poll(self) -> List[WorkflowStatusMessage]:
        with self._lock:
            batch = self._queue
            self._queue = []
        return batch
