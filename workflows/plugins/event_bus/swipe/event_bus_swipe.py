import json
from typing import Dict, List
import boto3
import os
from plugin_types import EventBus, WorkflowStatusMessage

SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "http://czidnet:5000/123456789012/swipe-test-notifications-sfn-notifications-queue") # TODO: remove hardcoded test


class EventBusSWIPE(EventBus):
    def __init__(self):
        self.sqs = boto3.client("sqs", endpoint_url="http://czidnet:5000")
        if SQS_QUEUE_URL and SQS_QUEUE_URL not in self.sqs.list_queues()["QueueUrls"]:
            raise Exception("SQS_QUEUE_URL not found")

    def retrieve_message(self, url: str) -> Dict:
        """Retrieve a single SQS message and delete it from queue"""
        resp = self.sqs.receive_message(
            QueueUrl=url,
            MaxNumberOfMessages=1,
        )
        # If no messages, just return
        if not resp.get("Messages", None):
            return {}

        message = resp["Messages"][0]
        receipt_handle = message["ReceiptHandle"]
        self.sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=receipt_handle,
        )
        return json.loads(message["Body"])
        
    async def send(self, message: WorkflowStatusMessage) -> None:
        pass

    
    async def poll(self) -> List[WorkflowStatusMessage]:
        if SQS_QUEUE_URL is None:
            return []

        message = self.retrieve_message(SQS_QUEUE_URL)
        workflow_statuses = []

        if message:
            print(message)
            if message["source"] == "aws.states":
                workflow_status = WorkflowStatusMessage(
                    runner_id=message["detail"]["executionArn"],
                    status=f'WORKFLOW_{message["detail"]["status"]}'
                )
                workflow_statuses.append(
                    workflow_status
                )
            elif message["source"] == "aws.batch":
                print("BAATTCH", message)
        return workflow_statuses
