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
    }
  }
  additional_env_vars = {
    AWS_REGION                                      = "us-west-2"
    BOTO_ENDPOINT_URL                               = "http://motoserver.czidnet:4000"
    CERBOS_URL                                      = "http://localhost:3592"
    DEFAULT_UPLOAD_BUCKET                           = "local-bucket"
    DEFAULT_UPLOAD_PROTOCOL                         = "s3"
    ENTITY_SERVICE_URL                              = "http://ryan-test-entities:8008"
    ENTITY_SERVICE_AUTH_TOKEN                       = "eyJhbGciOiJFQ0RILUVTIiwiZW5jIjoiQTI1NkNCQy1IUzUxMiIsImVwayI6eyJjcnYiOiJQLTM4NCIsImt0eSI6IkVDIiwieCI6IkNFSUZ5SmhHX09FRFpOYV9GN0NveFFMTWRnSy1vaW5wRVMxZmFQNHk5cC13ZU51c1JKVm9yMXJZbU5JdXh6ekgiLCJ5IjoicnRPM1FRYS1xRFR2VTNIa3IyUVQ5eE1kanpydzd0Y0xyVl9oSE4zVDdjRUVoQy00czg4ZE5mNU42SkxyM3YyeSJ9LCJraWQiOiItQmx2bF9wVk5LU2JRQ2N5dGV4UzNfMk5MaHBia2J6LVk5VFFjbkY5S1drIiwidHlwIjoiSldFIn0..9K7pNxXmTBf5fzX_H_Uqbw.87heaMhVrIb-ZO6jrbWtcR3c8kt8Otokten2nA6iX8LTOzDx2vqXaMd_8qoJd5UsbV409RTi67_hZ-cZKhL3wXxD_DkURU_y_qXl_alnyZBAdCMEy0LB_Uts4y88RFSh0Ke_RrFYg0MhH0AsMTPoBNQjCbbYaF-uFyW23pdOBzK2qFRpRy1BCLYBxBaVBU5wy05h58BY3Hzn1bDVMOXHbMgHniT3vKD-iM6ZsNiGbmC9GT59VSDLn0emzPBx3_xlk2cYk3ZwptGNXwaSH9Ez6z0gQTNtfDmE0aZzVypD7ZF_0tf5JBs30B5wk4xJdwmyXy_qazFJoOfIyT5rPvVuDbfXatD1fQ1UXDrB-_FU7asC58JNxkemgJ7onWrKs3CZk38HWkO0b7wBhSuGy8KnkLqQWv5y9NlIOaLQv2EpaeIRI22WTfxpwOhcDrw6RnB6DEdsogvpacLbWxohaOudfQl73rk-PfgN_VpPOXlFVHViMTGr83lLgXfCC_E-Q4GpOe_McCK1BQ-Qn0SBF32ofkAk6w5e348cHFUNc9VJ5QPqqzoZvYQJVcFD_FpPaETR.lWx9pYq25tJEory9WJMQTCtoEMwodVYNQA9O5qqQV6A"
    JWK_PRIVATE_KEY_FILE                            = "/workflows/test_infra/fixtures/private_key.pem"
    JWK_PUBLIC_KEY_FILE                             = "/workflows/test_infra/fixtures/public_key.pem"
    WORKERS                                         = "2"
    PLATFORMICS_WORKFLOW_RUNNER_PLUGIN              = "swipe"
    PLATFORMICS_EVENT_BUS_PLUGIN                    = "swipe"
    PLATFORMICS_WORKFLOW_RUNNER__LOCAL__S3_ENDPOINT = ""
    PLATFORMICS_WORKFLOW_RUNNER__SWIPE__OUTPUT_S3_PREFIX  = "s3://idseq-samples-development/nextgen/"
    PLATFORMICS_WORKFLOW_RUNNER__SWIPE__STATE_MACHINE_ARN = "arn:aws:states:us-west-2:732052188396:stateMachine:idseq-swipe-sandbox-default-wdl"
    PLATFORMICS_EVENT_BUS__SWIPE__SQS_QUEUE_URL     = "https://sqs.us-west-2.amazonaws.com/732052188396/idseq-swipe-staging-web-sfn-notifications-queue"
    PLATFORMICS_EVENT_BUS__REDIS__REDIS_URL         = "redis://redis.czidnet:6378"
    PLATFORMICS_EVENT_BUS__REDIS__QUEUE_NAME        = "workflow-events"
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
