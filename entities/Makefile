SHELL := /bin/bash

FOLDER = entities
CONTAINER ?= entities

### DOCKER ENVIRONMENTAL VARS #################################################
export DOCKER_BUILDKIT:=1
export COMPOSE_DOCKER_CLI_BUILD:=1
export docker_compose:=docker compose
export docker_compose_run:=docker compose run --rm

### DATABASE VARIABLES #################################################
SERVICE_NAME = entities
LOCAL_DB_NAME = platformics
LOCAL_DB_SERVER = localhost:5432
LOCAL_DB_USERNAME = postgres
LOCAL_DB_PASSWORD = password_postgres
LOCAL_DB_CONN_STRING = postgresql://$(LOCAL_DB_USERNAME):$(LOCAL_DB_PASSWORD)@$(LOCAL_DB_SERVER)/$(LOCAL_DB_NAME)$(SERVICE_NAME)

### HELPFUL #################################################

help: shared-help ## display help for this makefile
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

.PHONY: shared-help
shared-help: 
	$(MAKE) -f platformics/Makefile help

.PHONY: rm-pycache
rm-pycache: ## remove all __pycache__ files (run if encountering issues with pycharm debugger (containers exiting prematurely))
	find . -name '__pycache__' | xargs rm -rf

### DOCKER LOCAL DEV #########################################
.PHONY: local-setup
local-setup: ## Load db tables and seed data
	while [ -z "$$($(docker_compose) exec -T entities-db psql $(LOCAL_DB_CONN_STRING) -c 'select 1')" ]; do echo "waiting for db to start..."; sleep 1; done;
	$(docker_compose_run) entities alembic upgrade head
	$(MAKE) local-seed
	$(MAKE) codegen-test-schema

.PHONY: local-start
local-start: ## Start a local dev environment that's been stopped.
	$(docker_compose) up -d

.PHONY: local-init
local-init: local-start local-setup 

.PHONY: local-pgconsole
local-pgconsole: ## Connect to the local postgres database.
	$(docker_compose) exec entities-db psql "$(LOCAL_DB_CONN_STRING)"

.PHONY: local-tests
local-tests: ## Run entities tests
	$(MAKE) codegen-test-schema
	$(docker_compose_run) entities bash -c "poetry run pytest -s"
	$(MAKE) cerbos-tests

DIR_LINT_CODEGEN_TEST = platformics/codegen/tests/output/
.PHONY: codegen-test-schema
codegen-test-schema:  ## Run codegen on the test schema
	# Copy the default queries template into the test schema override dir so we're not trying to keep multiple copies in sync in git
	cp platformics/codegen/templates/api/queries.py.j2 platformics/codegen/tests/test_schemas/overrides/api/queries.py.j2
	# Add a little bit of extra code to the base Query class so we can use it in our tests
	cat platformics/codegen/tests/test_schemas/overrides/api/extra_test_code.py.j2 >> platformics/codegen/tests/test_schemas/overrides/api/queries.py.j2
	# Make sure the codegen CLI has a `template-override-dir` argument so it uses our modified template for queries.py
	$(docker_compose) exec entities python3 platformics/codegen/generator.py api generate --schemafile platformics/codegen/tests/test_schemas/platformics.yaml --template-override-paths platformics/codegen/tests/test_schemas/overrides --output-prefix $(DIR_LINT_CODEGEN_TEST)
	$(docker_compose_run) $(FOLDER) black  $(DIR_LINT_CODEGEN_TEST)
	$(docker_compose_run) $(FOLDER) ruff check --fix  $(DIR_LINT_CODEGEN_TEST)

DIR_LINT_CODEGEN = database/models/ api/types/ api/{queries,mutations}.py test_infra/factories/
DIR_LINT_GRAPHQL = cli/gql_schema.py
.PHONY: codegen
codegen:  ## Update the GQL types used by the CLI
	$(docker_compose) exec entities python3 platformics/codegen/generator.py api generate --schemafile schema/platformics.yaml --output-prefix .
	$(docker_compose_run) $(FOLDER) black $(DIR_LINT_CODEGEN)
	$(docker_compose_run) $(FOLDER) ruff check --fix $(DIR_LINT_CODEGEN)

	$(docker_compose_run) entities strawberry export-schema api.main:schema > api/schema.graphql
	$(docker_compose) exec entities python3 -m sgqlc.introspection --exclude-deprecated --exclude-description http://localhost:8008/graphql api/schema.json
	$(docker_compose) exec entities sgqlc-codegen schema api/schema.json cli/gql_schema.py
	$(docker_compose) exec entities sgqlc-codegen schema api/schema.json platformics/client/entities_schema.py
	$(docker_compose_run) $(FOLDER) black $(DIR_LINT_GRAPHQL)
	$(docker_compose_run) $(FOLDER) ruff check --fix $(DIR_LINT_GRAPHQL)

	$(docker_compose) exec entities gen-erdiagram schema/platformics.yaml > schema/README.md

### CERBOS #############################################
cerbos-tests:
	$(docker_compose_run) cerbos compile --tests=/var/policies/cerbos/test/ /var/policies/cerbos/policies

### SHARED MAKEFILE #############################################
%: 
	$(MAKE) -f platformics/Makefile $@ \
		FOLDER=$(FOLDER) \
		CONTAINER=$(CONTAINER) \
		LOCAL_DB_NAME=$(LOCAL_DB_NAME) \
		LOCAL_DB_SERVER=$(LOCAL_DB_SERVER) \
		LOCAL_DB_USERNAME=$(LOCAL_DB_USERNAME) \
		LOCAL_DB_PASSWORD=$(LOCAL_DB_PASSWORD) \
		LOCAL_DB_CONN_STRING=$(LOCAL_DB_CONN_STRING)
