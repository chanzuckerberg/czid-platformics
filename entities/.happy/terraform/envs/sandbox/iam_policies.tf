data "aws_iam_policy_document" "entities" {
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
}
