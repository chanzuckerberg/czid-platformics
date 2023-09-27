import unittest
import time
import json
import boto3
from workflow_runner_swipe import SwipeWorkflowRunner


class TestSFNWDL(unittest.TestCase):
    def setUp(self) -> None:
        self.s3 = boto3.resource("s3", endpoint_url="http://motoserver.czidnet:4000")
        self.test_bucket = self.s3.create_bucket(Bucket="swipe-test")

        self.batch = boto3.client("batch", endpoint_url="http://motoserver.czidnet:4000")
        self.logs = boto3.client("logs",  endpoint_url="http://motoserver.czidnet:4000")
        ## TODO Loop through multiple wdl files to read everything into the test bucket
        with open("terraform_test/test_wdl.wdl") as f:
            self.wdl_one = f.read()

        self.wdl_obj = self.test_bucket.Object("test_wdl.wdl")
        self.wdl_obj.put(Body=self.wdl_one.encode())

        self.input_obj = self.test_bucket.Object("input.txt")
        self.input_obj.put(Body="hello".encode())

    def print_execution(self, events):
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
                    if (
                        event.get("taskSubmittedEventDetails", {}).get("resourceType")
                        == "batch"
                    ):
                        job_id = json.loads(
                            event["taskSubmittedEventDetails"]["output"]
                        )["JobId"]
                        print(f"Batch job ID {job_id}", file=sys.stderr)
                        job_desc = self.batch.describe_jobs(jobs=[job_id])["jobs"][0]
                        try:
                            log_group_name = job_desc["container"]["logConfiguration"][
                                "options"
                            ]["awslogs-group"]
                        except KeyError:
                            log_group_name = "/aws/batch/job"
                        response = self.logs.get_log_events(
                            logGroupName=log_group_name,
                            logStreamName=job_desc["container"]["logStreamName"],
                        )
                        for log_event in response["events"]:
                            print(log_event["message"], file=sys.stderr)
                seen_events.add(event["id"])

    def test_simple_swipe_workflow(self):
        """A simple test to test whether the SWIPE plugin works"""
        workflow_runner = SwipeWorkflowRunner(f"s3://{self.wdl_obj.bucket_name}/")
        # TODO: Add listener function + workflow run when available
        workflow_output = workflow_runner.run_workflow(
            on_complete=lambda x: print(x),
            workflow_run_id=1,
            workflow_path=f"s3://{self.wdl_obj.bucket_name}/{self.wdl_obj.key}",
            inputs={
                "hello": f"s3://{self.input_obj.bucket_name}/{self.input_obj.key}",
                "docker_image_id": "ubuntu",
            },
        )
        workflow_json = json.loads(workflow_output)
        sfn = boto3.client("stepfunctions", endpoint_url="http://sfn.czidnet:8083")
        arn = workflow_json["response"]["executionArn"]
        breakout = 0
        while sfn.describe_execution(executionArn=arn)["status"] not in ["SUCCEEDED", "FAILED"]:
            time.sleep(1)
            breakout += 1
            if breakout == 120:
                # make sure weird conditions don't hang the tests
                break

        self.print_execution(sfn.get_execution_history(executionArn=arn)["events"])
        self.assertEqual(sfn.describe_execution(executionArn=arn)["status"], "SUCCEEDED")


if __name__ == "__main__":
    unittest.main()
