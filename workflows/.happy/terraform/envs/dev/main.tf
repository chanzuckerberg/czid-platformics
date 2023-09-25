# Auto-generated by 'happy infra'. Do not edit
# Make improvements in happy, so that everyone can benefit.
module "stack" {
  source           = "git@github.com:chanzuckerberg/happy//terraform/modules/happy-stack-eks?ref=main"
  image_tag        = var.image_tag
  stack_name       = var.stack_name
  k8s_namespace    = var.k8s_namespace
  image_tags       = jsondecode(var.image_tags)
  stack_prefix     = "/${var.stack_name}"
  app_name         = var.app
  deployment_stage = "dev"
  additional_env_vars = {
    CERBOS_URL = "http://cerbos.cerbos-system.svc.cluster.local:3592"
    JWK_PUBLIC_KEY_FILE = "/workflows/test_infra/fixtures/public_key.pem"
    JWK_PRIVATE_KEY_FILE = "/workflows/test_infra/fixtures/private_key.pem"
    DEFAULT_UPLOAD_BUCKET = "local-bucket"
    BOTO_ENDPOINT_URL = "http://motoserver.czidnet:4000"
    AWS_REGION = "us-west-2"
    ENTITY_SERVICE_URL = "http://entity-service:8080"
    ENTITY_SERVICE_AUTH_TOKEN = "test"
  }
  services = {
    workflows = {
      health_check_path     = "/graphql"
      name                  = "workflows"
      platform_architecture = "arm64"
      port                  = 8042
      priority              = 0
      service_type          = "PRIVATE"
      success_codes         = "200-499"
    }
  }
  create_dashboard = false
  routing_method   = "CONTEXT"

  tasks = {
    migrate = {
      image  = "{workflows}:${var.image_tag}"
      memory = "100Mi"
      cpu    = "100m"
      cmd    = ["/app/scripts/migrate.sh"]
    }
  }
}