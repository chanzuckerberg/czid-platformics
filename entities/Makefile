SHELL := /bin/bash

### DOCKER ENVIRONMENTAL VARS #################################################
export DOCKER_BUILDKIT:=1
export COMPOSE_DOCKER_CLI_BUILD:=1
export docker_compose:=docker compose

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
.PHONY: local-init
local-init:
	$(docker_compose) up -d
	while [ -z "$$($(docker_compose) exec -T postgres psql $(LOCAL_DB_CONN_STRING) -c 'select 1')" ]; do echo "waiting for db to start..."; sleep 1; done;
	$(docker_compose) run entities make alembic-upgrade-head
	$(MAKE) local-seed

.PHONY: debugger
debugger: ## Attach to the backend service (useful for pdb)
	docker attach $$($(docker_compose) ps | grep entities | cut -d ' ' -f 1 | head -n 1)

.PHONY: local-status
local-status: ## Show the status of the containers in the dev environment.
	docker ps -a | grep --color=no -e 'CONTAINER\|entities'

.PHONY: local-rebuild
local-rebuild: ## Rebuild local dev without re-importing data
	$(docker_compose) build
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
local-logs: ## Tail the logs of the dev env containers. ex: make local-logs CONTAINER=backend
	$(docker_compose) logs -f $(CONTAINER)

.PHONY: local-shell
local-shell: ## Open a command shell in one of the dev containers. ex: make local-shell CONTAINER=frontend
	$(docker_compose) exec $(CONTAINER) bash

.PHONY: local-pgconsole
local-pgconsole: ## Connect to the local postgres database.
	$(docker_compose) exec postgres psql "$(LOCAL_DB_CONN_STRING)"

.PHONY: local-update-backend-deps
local-update-backend-deps: ## Update poetry.lock to reflect pyproject.toml file changes.
	$(docker_compose) exec backend poetry update

.PHONY: local-tests
local-tests: local-seed ## Run entities tests
	$(docker_compose) run entities bash -c "poetry run pytest"

### GitHub Actions ###################################################
.PHONY: gha-setup
gha-setup:
	docker swarm init

### ALEMBIC #############################################
alembic-upgrade-head:
	alembic upgrade head # applies to local only

alembic-undo-migration:
	alembic downgrade -1

alembic-autogenerate:
	alembic revision --autogenerate -m "$(MESSAGE)" --rev-id $$(date +%Y%m%d_%H%M%S)
