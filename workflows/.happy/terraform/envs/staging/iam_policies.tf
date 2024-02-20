data "aws_iam_policy_document" "workflows" {
  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = ["arn:aws:ssm:us-west-2:${var.aws_account_id}:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
    ]
    resources = ["*"]
  }
}
