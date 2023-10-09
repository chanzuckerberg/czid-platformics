terraform {
  required_version = ">= 0.13.0"
  required_providers {
    aws = {
      version = "~> 3.28"
    }
  }
}

provider "aws" {
  endpoints {
    batch            = "http://localhost:4000"
    cloudwatch       = "http://localhost:4000"
    cloudwatchevents = "http://localhost:4000"
    ec2              = "http://localhost:4000"
    iam              = "http://localhost:4000"
    lambda           = "http://localhost:4000"
    s3               = "http://localhost:4000"
    secretsmanager   = "http://localhost:4000"
    sns              = "http://localhost:4000"
    sqs              = "http://localhost:4000"
    ssm              = "http://localhost:4000"
    stepfunctions    = "http://localhost:8083"
    sts              = "http://localhost:4000"
  }
}