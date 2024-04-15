""" 
Remote Event Bus plugin
Retrieves messages from AWS SQS
"""
import json
import logging
from typing import Awaitable, Callable, Optional, cast

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
from botocore.config import Config


class EventBusSWIPE(EventBus):
    def __init__(self, settings: SWIPEEventBusSettings) -> None:
        self._sqs = boto3.client("sqs", endpoint_url=settings.SQS_ENDPOINT)
        # increase max_attempts due to possible API throttling
        sfn_config = Config(
            retries={
                "max_attempts": 10,
                "mode": "standard",
            }
        )
        self._sfn = boto3.client("stepfunctions", endpoint_url=settings.SFN_ENDPOINT, config=sfn_config)
        #if settings.SQS_QUEUE_URL and settings.SQS_QUEUE_URL not in self._sqs.list_queues()["QueueUrls"]:
        #    raise Exception("SQS_QUEUE_URL not found")
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

    def _fetch_error(self, execution_arn: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
        try:
            desc = self._sfn.describe_execution(executionArn=execution_arn)
        except Exception as e:
            self._logger.warning(f"Could not describe execution {execution_arn}: ", exc_info=e)
            return "UnknownError", "Could not retrieve SFN error", None
        error = desc.get("error", None)
        cause = desc.get("cause", None)
        error_message = stack_trace = None
        try:
            parsed_cause = json.loads(cause)
            error_message = parsed_cause.get("errorMessage", None)
            stack_trace = parsed_cause.get("stackTrace", None)
        except json.JSONDecodeError:
            pass
        return error, error_message, stack_trace

    def _parse_message(self, message: dict) -> WorkflowStatusMessage | None:
        """Parse a message from SQS"""
        # TODO: handle aws.batch for step statuses
        if not message.get("source") == "aws.states":
            return None
        status = self._create_workflow_status(message["detail"]["status"])
        execution_arn = message["detail"]["executionArn"]
        if status == "WORKFLOW_SUCCESS":
            return WorkflowSucceededMessage(
                runner_id=execution_arn,
                outputs=json.loads(message["detail"]["output"])["Result"],
            )
        if status == "WORKFLOW_FAILURE":
            error, error_message, stack_trace = self._fetch_error(execution_arn)
            return WorkflowFailedMessage(
                runner_id=execution_arn,
                error=error,
                error_message=error_message,
                stack_trace=stack_trace and str(stack_trace),
            )
        if status == "WORKFLOW_STARTED":
            return WorkflowStartedMessage(
                runner_id=execution_arn,
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
