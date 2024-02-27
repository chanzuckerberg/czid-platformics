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
    resources = ["arn:aws:sqs:us-west-2:${var.aws_account_id}:idseq-swipe-development-web-sfn-notifications-queue"]
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
      "arn:aws:states:us-west-2:${var.aws_account_id}:stateMachine:idseq-swipe-development-default-wdl"
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
}
