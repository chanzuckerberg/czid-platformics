data "aws_iam_policy_document" "workflows" {
  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = ["arn:aws:secretsmanager:us-west-2:${var.aws_account_id}:secret:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
    ]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "sqs:DeleteMessage",
      "sqs:SendMessage",
      "sqs:ReceiveMessage"
    ]
    resources = ["arn:aws:sqs:us-west-2:${var.aws_account_id}:idseq-swipe-sandbox-nextgen-web-sfn-notifications-queue"]
  }
  statement {
    effect = "Allow"
    actions = [
      "sqs:ListQueues"
    ]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "states:DescribeExecution",
      "states:ListExecutions",
      "states:GetExecutionHistory",
      "states:StartExecution"
    ]
    resources = [
      "arn:aws:states:us-west-2:${var.aws_account_id}:stateMachine:idseq-swipe-sandbox-default-wdl",
      "arn:aws:states:us-west-2:${var.aws_account_id}:execution:idseq-swipe-sandbox-default-wdl:*",
      "arn:aws:states:us-west-2:${var.aws_account_id}:execution:idseq-swipe-sandbox-short-read-mngs-wdl:*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "states:ListStateMachines"
    ]
    resources = [
      "*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:DeleteObjectTagging",
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucketMultipartUploads",
      "s3:ListBucket",
      "s3:PutObjectTagging"
    ]
    resources = [
      "arn:aws:s3:::idseq-samples-development",
      "arn:aws:s3:::idseq-samples-sandbox",
      "arn:aws:s3:::idseq-samples-development/*",
      "arn:aws:s3:::idseq-samples-sandbox/*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:ListAllMyBuckets"
    ]
    resources = [
      "*"
    ]
  }
}
