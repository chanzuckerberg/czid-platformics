SHELL := /bin/bash

FOLDER = workflows
CONTAINER ?= workflows

# Sets .env.localdev file. [AWS|TEST] Otherwise sets an empty file
AWS_ENVIRONMENT ?= TEST 

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
help: shared-help ## display help for this makefile
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

.PHONY: shared-help
shared-help: 
	$(MAKE) -f platformics/Makefile help

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

.PHONY: local-swipe-plugin-tests
local-swipe-plugin-start: .env.localdev
	$(docker_compose) up --force-recreate -d 

.PHONY: local-swipe-plugin-deploy-mock
local-swipe-plugin-deploy-mock: local-swipe-plugin-start
	- source environment.test; aws ssm put-parameter --name /mock-aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id --value ami-12345678 --type String --endpoint-url http://localhost:4000 --no-cli-pager
	source environment.test && \
	cd terraform_test && \
	find . -name '*tfstate*' | xargs rm -f && \
	unset TF_CLI_ARGS_init && \
	terraform init && \
	terraform apply --auto-approve

.PHONY: local-swipe-plugin-tests
local-swipe-plugin-tests: local-swipe-plugin-deploy-mock
	$(docker_compose) exec workflows sh -c 'pytest terraform_test/'

DIR_LINT_CODEGEN = database/models/ api/types/ api/{queries,mutations}.py test_infra/factories/
DIR_LINT_GRAPHQL = cli/gql_schema.py
.PHONY: codegen
codegen:  ## Update the GQL types used by the CLI
	$(docker_compose) exec $(FOLDER) python3 platformics/codegen/generator.py api generate --schemafile schema/workflows.yaml --output-prefix . --skip-render-files
	$(docker_compose_run) $(FOLDER) black $(DIR_LINT_CODEGEN)
	$(docker_compose_run) $(FOLDER) ruff check --fix $(DIR_LINT_CODEGEN)

	$(docker_compose_run) $(FOLDER) strawberry export-schema api.main:schema > api/schema.graphql
	$(docker_compose) exec $(FOLDER) python3 -m sgqlc.introspection --exclude-deprecated --exclude-description http://localhost:8042/graphql api/schema.json
	$(docker_compose) exec $(FOLDER) sgqlc-codegen schema api/schema.json cli/gql_schema.py
	$(docker_compose_run) $(FOLDER) black $(DIR_LINT_GRAPHQL)
	$(docker_compose_run) $(FOLDER) ruff check --fix $(DIR_LINT_GRAPHQL)

	$(docker_compose) exec $(FOLDER) gen-erdiagram schema/workflows.yaml > schema/README.md

%: 
	$(MAKE) -f platformics/Makefile $@ \
		FOLDER=$(FOLDER) \
		CONTAINER=$(CONTAINER) \
		LOCAL_DB_NAME=$(LOCAL_DB_NAME) \
		LOCAL_DB_SERVER=$(LOCAL_DB_SERVER) \
		LOCAL_DB_USERNAME=$(LOCAL_DB_USERNAME) \
		LOCAL_DB_PASSWORD=$(LOCAL_DB_PASSWORD) \
		LOCAL_DB_CONN_STRING=$(LOCAL_DB_CONN_STRING)

