SHELL := /bin/bash

FOLDER = workflows
CONTAINER ?= workflows

# Sets .env.localdev file. [AWS|TEST] Otherwise sets an empty file
AWS_ENVIRONMENT ?= TEST 

MOTO_ENDPOINT_URL = http://localhost:4000

### DOCKER ENVIRONMENTAL VARS #################################################
export DOCKER_BUILDKIT:=1
export COMPOSE_DOCKER_CLI_BUILD:=1
export docker_compose:=docker compose --env-file .env.localdev
export docker_compose_run:=docker compose --env-file .env.localdev run --rm

### DATABASE VARIABLES #################################################
LOCAL_DB_NAME = workflows
LOCAL_DB_SERVER = localhost:5432
LOCAL_DB_USERNAME = postgres
LOCAL_DB_PASSWORD = password_postgres
LOCAL_DB_CONN_STRING = postgresql://$(LOCAL_DB_USERNAME):$(LOCAL_DB_PASSWORD)@$(LOCAL_DB_SERVER)/$(LOCAL_DB_NAME)


### HELPFUL #################################################
.PHONY: shared-help
shared-help: 
	$(MAKE) -f platformics/Makefile help

help: shared-help ## display help for this makefile
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

.env.localdev: 
	if [[ "$${AWS_ENVIRONMENT}" == "AWS" ]]; then \
		aws-oidc exec --session-duration=12h -- env | grep --color=no "AWS" > .env.localdev; \
	else \
		cp environment.test .env.localdev; \
	fi 

.PHONY: local-init
local-init: .env.localdev ## initialize service containers
	$(docker_compose) up -d
	while [ -z "$$($(docker_compose) exec -T postgres psql $(LOCAL_DB_CONN_STRING) -c 'select 1')" ]; do echo "waiting for db to start..."; sleep 1; done;
	$(docker_compose_run) $(FOLDER) alembic upgrade head
	$(MAKE) local-seed
	
.PHONY: local-start
local-start: .env.localdev ## Start a local dev environment that's been stopped.
	$(docker_compose) up -d 

.PHONY: local-pgconsole
local-pgconsole: ## Connect to the local postgres database.
	$(docker_compose) exec postgres psql "$(LOCAL_DB_CONN_STRING)"


.PHONY: local-db-tests
local-db-tests: ## Run workflow db tests
	$(docker_compose_run) $(FOLDER) bash -c "poetry run pytest test/"

### SWIPE Plugin Tests

.PHONY: local-swipe-plugin-clean
local-swipe-plugin-clean: ## Clean and reset infrastructure for running plugin tests
	- curl -X POST $(MOTO_ENDPOINT_URL)/moto-api/reset
	cd terraform_test && \
	find . -name '*tfstate*' | xargs rm -f && \
	rm -f ".terraform.lock.hcl" && \
	rm -rf ".terraform" && \
	unset TF_CLI_ARGS_init

.PHONY: local-swipe-plugin-start
local-swipe-plugin-start: .env.localdev ## Force restart containers
	$(docker_compose) up --force-recreate -d 

.PHONY: local-swipe-plugin-deploy-mock
local-swipe-plugin-deploy-mock: local-swipe-plugin-start local-swipe-plugin-clean ## Deploy SWIPE onto mock AWS infrastucture
	- source environment.test && \
	aws ssm put-parameter --name /mock-aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id \
	--value ami-12345678 --type String --endpoint-url $(MOTO_ENDPOINT_URL) --no-cli-pager && \
	cd terraform_test && \
	terraform init && \
	terraform apply --auto-approve

.PHONY: local-swipe-plugin-tests
local-swipe-plugin-tests: local-swipe-plugin-deploy-mock ## Run SWIPE plugin tests
	$(docker_compose) exec $(FOLDER) sh -c 'pytest terraform_test/'

%: 
	$(MAKE) -f platformics/Makefile $@ \
		FOLDER=$(FOLDER) \
		CONTAINER=$(CONTAINER) \
		LOCAL_DB_NAME=$(LOCAL_DB_NAME) \
		LOCAL_DB_SERVER=$(LOCAL_DB_SERVER) \
		LOCAL_DB_USERNAME=$(LOCAL_DB_USERNAME) \
		LOCAL_DB_PASSWORD=$(LOCAL_DB_PASSWORD) \
		LOCAL_DB_CONN_STRING=$(LOCAL_DB_CONN_STRING)

