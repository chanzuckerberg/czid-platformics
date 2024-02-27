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
  deployment_stage = "dev"
  services = {
    workflows = {
      aws_iam = {
        policy_json = data.aws_iam_policy_document.workflows.json,
      }
      name                  = "workflows"
      health_check_path     = "/graphql"
      platform_architecture = "arm64"
      port                  = 8042
      cpu                   = "2"
      memory                = "1000Mi"
      service_type          = "INTERNAL"

      init_containers = {
        init = {
          cmd   = ["cp", "-r", "/workflows/cerbos/", "/var/policies/"]
          image = "{workflows}"
          tag   = "${var.image_tag}" # manually modified as `happy infra generate` appended an extra $ to the front 
        },
        private-key = {
          cmd   = ["python3", "/czid-platformics/platformics/scripts/make_private_key_pem.py", "dev"]
          image = "{entities}"
          tag   = "${var.image_tag}"
        }
      }
      sidecars = {
        cerbos = {
          args   = ["server", "--config", "/var/policies/cerbos/config/config.yaml"]
          cpu    = "100m"
          image  = "ghcr.io/cerbos/cerbos"
          memory = "300Mi"
          port   = 3592
          tag    = "0.29.0"
        }
      }
    },
    workflows-worker = {
      aws_iam = {
        policy_json = data.aws_iam_policy_document.workflows.json,
      }
      cpu                   = "2"
      memory                = "1000Mi"
      name                  = "workflows-worker"
      platform_architecture = "arm64"
      service_type          = "PRIVATE"
      cmd                   = ["python3", "api/loader/run_loader.py"]
      port                  = 8000
    }
  }
  additional_env_vars = {
    AWS_REGION                                            = "us-west-2"
    BOTO_ENDPOINT_URL                                     = "http://motoserver.czidnet:4000"
    CERBOS_URL                                            = "http://localhost:3592"
    DEFAULT_UPLOAD_BUCKET                                 = "local-bucket"
    DEFAULT_UPLOAD_PROTOCOL                               = "s3"
    ENTITY_SERVICE_AUTH_TOKEN                             = ""
    ENTITY_SERVICE_URL                                    = "http://ryan-test-entities:8008"
    JWK_PRIVATE_KEY_FILE                                  = "/var/policies/private_key.pem"
    JWK_PUBLIC_KEY_FILE                                   = "/var/policies/public_key.pem"
    PLATFORMICS_EVENT_BUS_PLUGIN                          = "swipe"
    PLATFORMICS_EVENT_BUS__REDIS__QUEUE_NAME              = "workflow-events"
    PLATFORMICS_EVENT_BUS__REDIS__REDIS_URL               = "redis://redis.czidnet:6378"
    PLATFORMICS_EVENT_BUS__SWIPE__SQS_QUEUE_URL           = "https://sqs.us-west-2.amazonaws.com/732052188396/idseq-swipe-staging-web-sfn-notifications-queue"
    PLATFORMICS_WORKFLOW_RUNNER_PLUGIN                    = "swipe"
    PLATFORMICS_WORKFLOW_RUNNER__LOCAL__S3_ENDPOINT       = ""
    PLATFORMICS_WORKFLOW_RUNNER__SWIPE__OUTPUT_S3_PREFIX  = "s3://idseq-samples-development/nextgen/"
    PLATFORMICS_WORKFLOW_RUNNER__SWIPE__STATE_MACHINE_ARN = "arn:aws:states:us-west-2:732052188396:stateMachine:idseq-swipe-sandbox-default-wdl"
    WORKERS                                               = "2"
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
      cmd                   = ["/workflows/scripts/migrate.sh"]
      cpu                   = "100m"
      image                 = "{workflows}:${var.image_tag}"
      memory                = "1000Mi"
      platform_architecture = "arm64"
    }
  }
}
