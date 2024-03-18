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
          cmd   = ["python3", "/workflows/platformics/scripts/make_private_key_pem.py", "prod"]
          image = "{workflows}"
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
      init_containers = {
        private-key = {
          cmd   = ["python3", "/workflows/platformics/scripts/make_private_key_pem.py", "prod"]
          image = "{workflows-worker}"
          tag   = "${var.image_tag}"
        }
      }
    }
  }
  additional_env_vars = {
    AWS_REGION                                            = "us-west-2"
    CERBOS_URL                                            = "http://localhost:3592"
    DEFAULT_UPLOAD_BUCKET                                 = "local-bucket"
    DEFAULT_UPLOAD_PROTOCOL                               = "s3"
    IDENTITY_SERVICE_BASE_URL                             = "http://czid.org"
    ENTITY_SERVICE_URL                                    = "http://entities-entities:8008"
    ENTITY_SERVICE_AUTH_TOKEN                             = ""
    JWK_PRIVATE_KEY_FILE                                  = "/var/policies/private_key.pem"
    JWK_PUBLIC_KEY_FILE                                   = "/var/policies/public_key.pem"
    WORKERS                                               = "2"
    PLATFORMICS_WORKFLOW_RUNNER_PLUGIN                    = "swipe"
    PLATFORMICS_EVENT_BUS_PLUGIN                          = "swipe"
    PLATFORMICS_WORKFLOW_RUNNER__LOCAL__S3_ENDPOINT       = ""
    PLATFORMICS_WORKFLOW_RUNNER__SWIPE__OUTPUT_S3_PREFIX  = "s3://idseq-prod-samples-us-west-2/nextgen/"
    PLATFORMICS_WORKFLOW_RUNNER__SWIPE__STATE_MACHINE_ARN = "arn:aws:states:us-west-2:${var.aws_account_id}:stateMachine:idseq-swipe-prod-default-wdl"
    PLATFORMICS_EVENT_BUS__SWIPE__SQS_QUEUE_URL           = "https://sqs.us-west-2.amazonaws.com/${var.aws_account_id}/idseq-swipe-prod-nextgen-web-sfn-notifications-queue"
    PLATFORMICS_EVENT_BUS__REDIS__REDIS_URL               = "redis://redis.czidnet:6378"
    PLATFORMICS_EVENT_BUS__REDIS__QUEUE_NAME              = "workflow-events"
    SERVICE_NAME                                          = "workflows"
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
