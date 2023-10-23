SHELL := /bin/bash

FOLDER = workflows
CONTAINER ?= workflows

MOTO_SERVER_PATH=http://localhost:4000
### DOCKER ENVIRONMENTAL VARS #################################################
export DOCKER_BUILDKIT:=1
export COMPOSE_DOCKER_CLI_BUILD:=1
export docker_compose:=docker compose
export docker_compose_run:=docker compose run --rm

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

.PHONY: local-swipe-plugin-tests
local-swipe-plugin-start:
	source environment.test; $(docker_compose) up --force-recreate -d 

.PHONY: local-swipe-plugin-deploy-mock
local-swipe-plugin-deploy-mock: local-swipe-plugin-start local-swipe-plugin-reset
	- source environment.test && \
	aws ssm put-parameter --name /mock-aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id \
		--value ami-12345678 --type String --endpoint-url $(MOTO_SERVER_PATH) \
		--no-cli-pager && \
	cd terraform_test && \
	unset TF_CLI_ARGS_init && \
	terraform init && \
	terraform apply --auto-approve

.PHONY: local-swipe-plugin-reset
local-swipe-plugin-reset: 
	- curl -X POST $(MOTO_SERVER_PATH)/moto-api/reset &&\
	cd terraform_test && \
	find . -name '*tfstate*' | xargs rm -f 


.PHONY: local-swipe-plugin-tests
local-swipe-plugin-tests: local-swipe-plugin-deploy-mock
	$(docker_compose) exec workflows sh -c 'pytest terraform_test/'

%: 
	$(MAKE) -f platformics/Makefile $@ \
		FOLDER=$(FOLDER) \
		CONTAINER=$(CONTAINER) \
		LOCAL_DB_NAME=$(LOCAL_DB_NAME) \
		LOCAL_DB_SERVER=$(LOCAL_DB_SERVER) \
		LOCAL_DB_USERNAME=$(LOCAL_DB_USERNAME) \
		LOCAL_DB_PASSWORD=$(LOCAL_DB_PASSWORD) \
		LOCAL_DB_CONN_STRING=$(LOCAL_DB_CONN_STRING)

