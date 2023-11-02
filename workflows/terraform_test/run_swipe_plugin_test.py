import unittest
import time
import json
import boto3
from typing import Dict, List, Any
from workflow_runner_swipe import SwipeWorkflowRunner


class AWSMock:
    def __init__(
        self,
        endpoint_url: str = "http://motoserver.czidnet:4000",
        sfn_endpoint_url: str = "http://sfn.czidnet:8083",
        aws_region: str = "us-east-1",
    ) -> None:
        self.s3 = boto3.resource("s3", endpoint_url=endpoint_url, region_name=aws_region)
        self.sqs = boto3.client("sqs", endpoint_url=endpoint_url, region_name=aws_region)
        self.sfn = boto3.client("stepfunctions", endpoint_url=sfn_endpoint_url, region_name=aws_region)

    def get_sqs_url(self) -> str:
        return self.sqs.list_queues()["QueueUrls"][0]

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

    def get_sfn_execution_status(self, sfn_arn: str) -> List:
        return self.sfn.describe_execution(executionArn=sfn_arn)["status"]


class TestSFNWDL(unittest.TestCase):
    def setUp(self) -> None:
        self.s3 = boto3.resource("s3", endpoint_url="http://motoserver.czidnet:4000")
        self.test_bucket = self.s3.create_bucket(Bucket="swipe-test")

        self.batch = boto3.client("batch", endpoint_url="http://motoserver.czidnet:4000")
        self.logs = boto3.client("logs", endpoint_url="http://motoserver.czidnet:4000")
        ## TODO Loop through multiple wdl files to read everything into the test bucket
        with open("terraform_test/test_wdl.wdl") as f:
            self.wdl_one = f.read()

        self.wdl_obj = self.test_bucket.Object("test_wdl.wdl")
        self.wdl_obj.put(Body=self.wdl_one.encode())

        self.input_obj = self.test_bucket.Object("input.txt")
        self.input_obj.put(Body="hello".encode())
        self.aws = AWSMock()

    def print_execution(self, events: List[Any]) -> None:
        import sys

        seen_events = set()
        for event in sorted(
            events,
            key=lambda x: x["id"],
        ):
            if event["id"] not in seen_events:
                details = {}
                for key in event.keys():
                    if key.endswith("EventDetails") and event[key]:
                        details = event[key]
                print(
                    event["timestamp"],
                    event["type"],
                    details.get("resourceType", ""),
                    details.get("resource", ""),
                    details.get("name", ""),
                    json.loads(details.get("parameters", "{}")).get("FunctionName", ""),
                    file=sys.stderr,
                )
                if "taskSubmittedEventDetails" in event:
                    if event.get("taskSubmittedEventDetails", {}).get("resourceType") == "batch":
                        job_id = json.loads(event["taskSubmittedEventDetails"]["output"])["JobId"]
                        print(f"Batch job ID {job_id}", file=sys.stderr)
                        job_desc = self.batch.describe_jobs(jobs=[job_id])["jobs"][0]
                        try:
                            log_group_name = job_desc["container"]["logConfiguration"]["options"]["awslogs-group"]
                        except KeyError:
                            log_group_name = "/aws/batch/job"
                        response = self.logs.get_log_events(
                            logGroupName=log_group_name,
                            logStreamName=job_desc["container"]["logStreamName"],
                        )
                        for log_event in response["events"]:
                            print(log_event["message"], file=sys.stderr)
                seen_events.add(event["id"])
    
    def test_simple_swipe_workflow(self) -> None:
        """A simple test to test whether the SWIPE plugin works"""
        workflow_runner = SwipeWorkflowRunner(f"s3://{self.wdl_obj.bucket_name}/")
        # TODO: Add listener function + workflow run when available
        workflow_output = workflow_runner.run_workflow(
            event_bus= "",
            workflow_path=f"s3://{self.wdl_obj.bucket_name}/{self.wdl_obj.key}",
            inputs={
                "hello": f"s3://{self.input_obj.bucket_name}/{self.input_obj.key}",
                "docker_image_id": "ubuntu",
            },
        )
        workflow_json = json.loads(workflow_output)

        breakout = 0
        while (arn := self.aws.get_sfn_execution_status(workflow_json["response"]["executionArn"])) not in [
            "SUCCEEDED",
            "FAILED",
        ]:
            time.sleep(1)
            breakout += 1
            if breakout == 120:
                # make sure weird conditions don't hang the tests
                break

        step_notifications = []
        stage_notifications = []
        while message := self.aws.retrieve_message(self.aws.get_sqs_url()):
            if message["source"] == "aws.batch":
                step_notifications.append(message["detail"])
            elif message["source"] == "aws.states":
                stage_notifications.append(message["detail"])

        self.assertEqual(arn, "SUCCEEDED")
        self.assertEqual(len(step_notifications), 3)
        self.assertEqual(len(stage_notifications), 1)


if __name__ == "__main__":
    unittest.main()
