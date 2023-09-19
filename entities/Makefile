SHELL := /bin/bash

### DOCKER ENVIRONMENTAL VARS #################################################
export DOCKER_BUILDKIT:=1
export COMPOSE_DOCKER_CLI_BUILD:=1
export docker_compose:=docker compose
export docker_compose_run:=docker compose run --rm

### DATABASE VARIABLES #################################################
LOCAL_DB_NAME = entities
LOCAL_DB_SERVER = localhost:5432
LOCAL_DB_USERNAME = postgres
LOCAL_DB_PASSWORD = password_postgres
LOCAL_DB_CONN_STRING = postgresql://$(LOCAL_DB_USERNAME):$(LOCAL_DB_PASSWORD)@$(LOCAL_DB_SERVER)/$(LOCAL_DB_NAME)

### HELPFUL #################################################
help: ## display help for this makefile
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

.PHONY: rm-pycache
rm-pycache: ## remove all __pycache__ files (run if encountering issues with pycharm debugger (containers exiting prematurely))
	find . -name '__pycache__' | xargs rm -rf

### DOCKER LOCAL DEV #########################################
.PHONY: local-setup
local-setup: ## Load db tables and seed data
	while [ -z "$$($(docker_compose) exec -T entities-db psql $(LOCAL_DB_CONN_STRING) -c 'select 1')" ]; do echo "waiting for db to start..."; sleep 1; done;
	$(docker_compose_run) entities alembic upgrade head
	$(MAKE) local-seed

.PHONY: local-init
local-init: local-start local-setup ## Setup a working local-dev environment

.PHONY: debugger
debugger: ## Attach to the gql service (useful for pdb)
	docker attach $$($(docker_compose) ps | grep entities | cut -d ' ' -f 1 | head -n 1)

.PHONY: local-status
local-status: ## Show the status of the containers in the dev environment.
	docker ps -a | grep --color=no -e 'CONTAINER\|entities'

.PHONY: local-build
local-build: ## Build images
	$(docker_compose) build

.PHONY: local-rebuild
local-rebuild: local-build ## Rebuild local dev without re-importing data
	$(docker_compose) up -d

.PHONY: local-sync
local-sync: local-rebuild local-init ## Re-sync the local-environment state after modifying library deps or docker configs

.PHONY: local-start
local-start: ## Start a local dev environment that's been stopped.
	$(docker_compose) up -d

.PHONY: local-stop
local-stop: ## Stop the local dev environment.
	$(docker_compose) --profile '*' stop

.PHONY: local-clean
local-clean: local-stop ## Remove everything related to the local dev environment (including db data!)
	$(docker_compose) down

.PHONY: local-seed
local-seed: ## Seed the dev db with a reasonable set of starting data.
	$(docker_compose) exec entities python3 scripts/seed.py

.PHONY: local-logs
local-logs: ## Tail the logs of the dev env containers. ex: make local-logs CONTAINER=entities
	$(docker_compose) logs -f $(CONTAINER)

.PHONY: local-shell
local-shell: ## Open a command shell in one of the dev containers. ex: make local-shell CONTAINER=frontend
	$(docker_compose) exec $(CONTAINER) bash

.PHONY: local-pgconsole
local-pgconsole: ## Connect to the local postgres database.
	$(docker_compose) exec entities-db psql "$(LOCAL_DB_CONN_STRING)"

.PHONY: local-update-deps
local-update-deps: ## Update poetry.lock to reflect pyproject.toml file changes.
	$(docker_compose) exec entities poetry update

.PHONY: local-tests
local-tests: ## Run entities tests
	$(docker_compose_run) entities bash -c "poetry run pytest -s"
	$(MAKE) cerbos-tests

.PHONY: local-token
local-token: ## Copy an auth token for this local dev env to the system clipboard
	TOKEN=$$($(docker_compose_run) entities ./cli/gqlcli.py auth generate-token 111 --project 444:admin --expiration 99999); echo '{"Authorization":"Bearer '$$TOKEN'"}' | tee >(pbcopy)

.PHONY: fix-poetry-lock
fix-poetry-lock: ## Fix poetry lockfile after merge conflict & repairing pyproject.toml
	git checkout --theirs poetry.lock
	$(docker_compose_run) entities poetry lock --no-update

.PHONY: fix-lint
fix-lint: ## Apply linting rules to the code in this directory.
	$(docker_compose_run) entities black .
	$(docker_compose_run) entities ruff check --fix .

.PHONY: check-lint
check-lint: ## Check for bad linting
	$(docker_compose_run) entities black --check .
	$(docker_compose_run) entities ruff check .
	$(docker_compose_run) entities mypy .

.PHONY: local-mypy
local-mypy: ## Run type checking
	$(docker_compose) exec entities mypy .

.PHONY: codegen
codegen:  ## Update the GQL types used by the CLI
	$(docker_compose_run) entities strawberry export-schema api.main:schema > api/schema.graphql
	$(docker_compose) exec entities python3 -m sgqlc.introspection --exclude-deprecated --exclude-description http://localhost:8008/graphql api/schema.json
	$(docker_compose) exec entities sgqlc-codegen schema api/schema.json cli/gql_schema.py
	cp cli/gql_schema.py ../workflows/entity_gql_schema.py

### GitHub Actions ###################################################
.PHONY: gha-setup
gha-setup:
	docker swarm init

### ALEMBIC #############################################
alembic-upgrade-head:
	$(docker_compose) exec entities alembic upgrade head ## Run alembic migrations locally

alembic-undo-migration: ## Downgrade the latest alembic migration
	$(docker_compose) exec entities alembic downgrade -1

alembic-autogenerate: ## Create new alembic migrations files based on SA schema changes.
	$(docker_compose) exec entities alembic revision --autogenerate -m "$(MESSAGE)" --rev-id $$(date +%Y%m%d_%H%M%S)

### CERBOS #############################################
cerbos-tests:
	$(docker_compose_run) cerbos compile --tests=/entities/test/ /entities/policies
