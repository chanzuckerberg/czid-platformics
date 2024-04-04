# Auto-generated by 'happy infra'. Do not edit
# Make improvements in happy, so that everyone can benefit.
module "stack" {
  source           = "git@github.com:chanzuckerberg/happy//terraform/modules/happy-stack-eks?ref=rlim/ephemeral-volume-support"
  image_tag        = var.image_tag
  stack_name       = var.stack_name
  k8s_namespace    = var.k8s_namespace
  image_tags       = jsondecode(var.image_tags)
  stack_prefix     = "/${var.stack_name}"
  app_name         = var.app
  deployment_stage = "prod"
  services = {
    entities = {
      aws_iam = {
        policy_json = data.aws_iam_policy_document.entities.json,
      }
      cpu               = "8"
      health_check_path = "/graphql"
      init_containers = {
        init = {
          cmd   = ["cp", "-r", "/czid-platformics/entities/cerbos/", "/var/policies/"]
          image = "{entities}"
          tag   = "${var.image_tag}"
        },
        private-key = {
          cmd   = ["python3", "/czid-platformics/platformics/scripts/make_private_key_pem.py", "prod"]
          image = "{entities}"
          tag   = "${var.image_tag}"
        }
      }
      memory                = "8000Mi"
      name                  = "entities"
      platform_architecture = "arm64"
      port                  = 8008
      service_type          = "INTERNAL"
      sidecars = {
        cerbos = {
          args   = ["server", "--config", "/var/policies/cerbos/config/config.yaml"]
          cpu    = "400m"
          image  = "ghcr.io/cerbos/cerbos"
          memory = "300Mi"
          port   = 3592
          tag    = "0.29.0"
        }
      }
    }
  }
  additional_env_vars = {
    AWS_REGION              = "us-west-2"
    CERBOS_URL              = "http://localhost:3592"
    DEFAULT_UPLOAD_BUCKET   = "local-bucket"
    DEFAULT_UPLOAD_PROTOCOL = "s3"
    JWK_PRIVATE_KEY_FILE    = "/var/policies/private_key.pem"
    JWK_PUBLIC_KEY_FILE     = "/var/policies/public_key.pem"
    WORKERS                 = "2"
  }
  create_dashboard = false
  emptydir_volumes = [{
    name = "policies"
    parameters = {
      size_limit = "100Mi"
    }
  }]
  routing_method = "CONTEXT"
  tasks = {
    migrate = {
      cmd                   = ["/czid-platformics/entities/scripts/migrate.sh"]
      cpu                   = "400m"
      image                 = "{entities}:${var.image_tag}"
      memory                = "2000Mi"
      platform_architecture = "arm64"
    }
  }
}