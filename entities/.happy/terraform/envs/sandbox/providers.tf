# Auto-generated by 'happy infra'. Do not edit
# Make improvements in happy, so that everyone can benefit.
provider "aws" {
  region = "us-west-2"
  assume_role {
    role_arn = "arn:aws:iam::${var.aws_account_id}:role/${var.aws_role}"
  }
  default_tags {
    tags = {
      TFC_RUN_ID                               = coalesce(var.TFC_RUN_ID, "unknown")
      TFC_WORKSPACE_NAME                       = coalesce(var.TFC_WORKSPACE_NAME, "unknown")
      TFC_WORKSPACE_SLUG                       = coalesce(var.TFC_WORKSPACE_SLUG, "unknown")
      TFC_CONFIGURATION_VERSION_GIT_BRANCH     = coalesce(var.TFC_CONFIGURATION_VERSION_GIT_BRANCH, "unknown")
      TFC_CONFIGURATION_VERSION_GIT_COMMIT_SHA = coalesce(var.TFC_CONFIGURATION_VERSION_GIT_COMMIT_SHA, "unknown")
      TFC_CONFIGURATION_VERSION_GIT_TAG        = coalesce(var.TFC_CONFIGURATION_VERSION_GIT_TAG, "unknown")
      TFC_PROJECT_NAME                         = coalesce(var.TFC_PROJECT_NAME, "unknown")
      project                                  = coalesce(var.project, "unknown")
      env                                      = coalesce(var.env, "unknown")
      service                                  = coalesce(var.service, "unknown")
      owner                                    = coalesce(var.owner, "unknown")
      managedBy                                = "terraform"
    }
  }
  allowed_account_ids = ["${var.aws_account_id}"]
}
provider "aws" {
  alias  = "czi-si"
  region = "us-west-2"
  assume_role {
    role_arn = "arn:aws:iam::626314663667:role/tfe-si"
  }
  default_tags {
    tags = {
      TFC_RUN_ID                               = coalesce(var.TFC_RUN_ID, "unknown")
      TFC_WORKSPACE_NAME                       = coalesce(var.TFC_WORKSPACE_NAME, "unknown")
      TFC_WORKSPACE_SLUG                       = coalesce(var.TFC_WORKSPACE_SLUG, "unknown")
      TFC_CONFIGURATION_VERSION_GIT_BRANCH     = coalesce(var.TFC_CONFIGURATION_VERSION_GIT_BRANCH, "unknown")
      TFC_CONFIGURATION_VERSION_GIT_COMMIT_SHA = coalesce(var.TFC_CONFIGURATION_VERSION_GIT_COMMIT_SHA, "unknown")
      TFC_CONFIGURATION_VERSION_GIT_TAG        = coalesce(var.TFC_CONFIGURATION_VERSION_GIT_TAG, "unknown")
      TFC_PROJECT_NAME                         = coalesce(var.TFC_PROJECT_NAME, "unknown")
      project                                  = coalesce(var.project, "unknown")
      env                                      = coalesce(var.env, "unknown")
      service                                  = coalesce(var.service, "unknown")
      owner                                    = coalesce(var.owner, "unknown")
      managedBy                                = "terraform"
    }
  }
  allowed_account_ids = ["626314663667"]
}
data "aws_eks_cluster" "cluster" {
  name = var.k8s_cluster_id
}
data "aws_eks_cluster_auth" "cluster" {
  name = var.k8s_cluster_id
}
provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}
data "kubernetes_namespace" "happy-namespace" {
  metadata {
    name = var.k8s_namespace
  }
}
data "aws_ssm_parameter" "dd_app_key" {
  name     = "/shared-infra-prod-datadog/app_key"
  provider = aws.czi-si
}
data "aws_ssm_parameter" "dd_api_key" {
  name     = "/shared-infra-prod-datadog/api_key"
  provider = aws.czi-si
}
provider "datadog" {
  app_key = data.aws_ssm_parameter.dd_app_key.value
  api_key = data.aws_ssm_parameter.dd_api_key.value
}
