""" 
Remote Event Bus plugin
Retrieves messages from AWS SQS
"""
import json
from typing import List, cast
import boto3
from settings import SWIPEEventBusSettings
import uuid
from plugins.plugin_types import (
    EventBus,
    WorkflowStartedMessage,
    WorkflowStatusMessage,
    WorkflowSucceededMessage,
    WorkflowFailedMessage,
    WorkflowStatus,
)


class EventBusSWIPE(EventBus):
    def __init__(self, settings: SWIPEEventBusSettings) -> None:
        self.sqs = boto3.client("sqs", endpoint_url=settings.SQS_ENDPOINT)
        self.settings = settings
        if settings.SQS_QUEUE_URL and settings.SQS_QUEUE_URL not in self.sqs.list_queues()["QueueUrls"]:
            raise Exception("SQS_QUEUE_URL not found")

    def valid_uuid(self, execution_id) -> bool:
        try:
            uuid.UUID(execution_id, version=4)
            return True
        except ValueError:
            return False

    def retrieve_messages(self, url: str) -> List:
        """Retrieve a list of SQS messages and delete them from queue"""
        resp = self.sqs.receive_message(
            QueueUrl=url,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=5,
        )
        # If no messages, just return
        if not resp.get("Messages", None):
            return []

        messages = []
        for message in resp["Messages"]:
            receipt_handle = message["ReceiptHandle"]
            body = json.loads(message["Body"])
            content = json.loads(body["Message"]) if body.get("Message") else body

            # check if message has valid uuid. If not could be from legacy web app
            if self.valid_uuid(content["detail"]["executionArn"].split(":")[-1]):
                messages.append(content)
                self.sqs.delete_message(
                    QueueUrl=url,
                    ReceiptHandle=receipt_handle,
                )

        return messages

    def create_workflow_status(self, status: str) -> WorkflowStatus:
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

    async def send(self, message: WorkflowStatusMessage) -> None:
        pass

    async def poll(self) -> List[WorkflowStatusMessage]:
        if self.settings.SQS_QUEUE_URL is None:
            return []

        messages = self.retrieve_messages(self.settings.SQS_QUEUE_URL)
        workflow_statuses: list[WorkflowStatusMessage] = []

        for message in messages:
            if message.get("source") == "aws.states":
                status = self.create_workflow_status(message["detail"]["status"])
                if status == "WORKFLOW_SUCCESS":
                    print("messsage detail", message["detail"]["output"])
                    workflow_statuses.append(
                        WorkflowSucceededMessage(
                            runner_id=message["detail"]["executionArn"],
                            outputs=json.loads(message["detail"]["output"])["Result"],
                        )
                    )
                if status == "WORKFLOW_FAILURE":
                    workflow_statuses.append(
                        WorkflowFailedMessage(
                            runner_id=message["detail"]["executionArn"],
                        )
                    )
                if status == "WORKFLOW_STARTED":
                    workflow_statuses.append(
                        WorkflowStartedMessage(
                            runner_id=message["detail"]["executionArn"],
                        )
                    )
            elif message.get("source") == "aws.batch":
                # TODO: return step status messages
                pass

        return workflow_statuses
