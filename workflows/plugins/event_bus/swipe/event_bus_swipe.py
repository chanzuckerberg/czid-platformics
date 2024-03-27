""" 
Remote Event Bus plugin
Retrieves messages from AWS SQS
"""
import json
import logging
from typing import Awaitable, Callable, cast

from settings import SWIPEEventBusSettings
from plugins.plugin_types import (
    EventBus,
    WorkflowStartedMessage,
    WorkflowStatusMessage,
    WorkflowSucceededMessage,
    WorkflowFailedMessage,
    WorkflowStatus,
)

import boto3


class EventBusSWIPE(EventBus):
    def __init__(self, settings: SWIPEEventBusSettings) -> None:
        self._sqs = boto3.client("sqs", endpoint_url=settings.SQS_ENDPOINT)
        if settings.SQS_QUEUE_URL and settings.SQS_QUEUE_URL not in self._sqs.list_queues()["QueueUrls"]:
            raise Exception("SQS_QUEUE_URL not found")
        self._sqs_queue_url = settings.SQS_QUEUE_URL
        self._logger = logging.getLogger("EventBusSWIPE")

    def _create_workflow_status(self, status: str) -> WorkflowStatus:
        """maps the SFN status to a workflow status"""
        return cast(
            WorkflowStatus,
            {
                "RUNNING": "WORKFLOW_STARTED",
                "SUCCEEDED": "WORKFLOW_SUCCESS",
                "FAILED": "WORKFLOW_FAILURE",
                "TIMED_OUT": "WORKFLOW_FAILURE",
                "ABORTED": "WORKFLOW_FAILURE",
            }.get(status),
        )

    def _parse_message(self, message: dict) -> WorkflowStatusMessage | None:
        """Parse a message from SQS"""
        # TODO: handle aws.batch for step statuses
        if not message.get("source") == "aws.states":
            return None
        status = self._create_workflow_status(message["status"])
        if status == "WORKFLOW_SUCCESS":
            return WorkflowSucceededMessage(
                runner_id=message["detail"]["executionArn"],
                outputs=json.loads(message["detail"]["output"])["Result"],
            )
        if status == "WORKFLOW_FAILURE":
            return WorkflowFailedMessage(
                runner_id=message["detail"]["executionArn"],
            )
        if status == "WORKFLOW_STARTED":
            return WorkflowStartedMessage(
                runner_id=message["detail"]["executionArn"],
            )
        return None

    async def send(self, message: WorkflowStatusMessage) -> None:
        """
        The SWIPE WorkflowRunner does not need to send messages
        """
        raise NotImplementedError

    async def poll(self, handle_message: Callable[[WorkflowStatusMessage], Awaitable[None]]) -> None:
        resp = self._sqs.receive_message(
            QueueUrl=self._sqs_queue_url,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=5,
        )

        # If no messages, just return
        if not resp.get("Messages", None):
            return

        for message in resp["Messages"]:
            message_id = message["MessageId"]
            receipt_handle = message["ReceiptHandle"]
            body = json.loads(message["Body"])
            content = json.loads(body["Message"]) if body.get("Message") else body
            parsed_message = self._parse_message(content)
            if not parsed_message:
                continue
            try:
                await handle_message(parsed_message)
                self._sqs.delete_message(
                    QueueUrl=self._sqs_queue_url,
                    ReceiptHandle=receipt_handle,
                )
            except Exception as e:
                self._logger.warn(f"Failed to handle message {message_id}: {e}")
                self._logger.exception(e)
