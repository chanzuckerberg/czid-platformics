SHELL := /bin/bash

FOLDER = workflows

# Sets .env.localdev file. [AWS|TEST] Otherwise sets an empty file
AWS_ENVIRONMENT ?= AWS 

### DOCKER ENVIRONMENTAL VARS #################################################
export DOCKER_BUILDKIT:=1
export COMPOSE_DOCKER_CLI_BUILD:=1
export docker_compose:=docker compose

### DATABASE VARIABLES #################################################
LOCAL_DB_NAME = workflows
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
	$(docker_compose) run $(FOLDER) alembic upgrade head
	$(MAKE) local-seed

.PHONY: debugger
debugger: ## Attach to the backend service (useful for pdb)
	docker attach $$($(docker_compose) ps | grep $(FOLDER) | cut -d ' ' -f 1 | head -n 1) --detach-keys="ctrl-p"

.PHONY: local-status
local-status: ## Show the status of the containers in the dev environment.
	docker ps -a | grep --color=no -e 'CONTAINER\|$(FOLDER)'

.PHONY: local-rebuild
local-rebuild: ## Rebuild local dev without re-importing data
	$(docker_compose) build

.PHONY: local-sync
local-sync: local-rebuild local-init ## Re-sync the local-environment state after modifying library deps or docker configs

.PHONY: local-envfile
local-envfile: 
	if [[ "$${AWS_ENVIRONMENT}" == "AWS" ]]; then \
		aws-oidc exec --session-duration=12h -- env | grep --color=no "AWS" > .env.localdev; \
	elif [[ "$${AWS_ENVIRONMENT}" == "TEST" ]]; then \
		cp environment.test .env.localdev; \
	else \
		> .env.localdev; \
	fi 

.PHONY: local-start
local-start: local-envfile ## Start a local dev environment that's been stopped.
	$(docker_compose) --env-file .env.localdev up -d 

.PHONY: local-stop
local-stop: ## Stop the local dev environment.
	$(docker_compose) --profile '*' stop

.PHONY: local-clean
local-clean: local-stop ## Remove everything related to the local dev environment (including db data!)
	$(docker_compose) down

.PHONY: local-seed
local-seed: ## Seed the dev db with a reasonable set of starting data.
	$(docker_compose) exec $(FOLDER) python3 scripts/seed.py

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
local-tests: ## Run tests
	$(docker_compose) run $(FOLDER) bash -c "poetry run pytest"

.PHONY: local-gqlschema
local-gqlschema: ## Export this app's GQL schema.
	$(docker_compose) run entities strawberry export-schema api.main:schema > api/schema.graphql

.PHONY: fix-lint
fix-lint: ## Apply linting rules to the code in this directory.
	$(docker_compose) run entities black .
	$(docker_compose) run entities ruff check --fix .

.PHONY: update-cli
update-cli:  ## Update the GQL types used by the CLI
	$(docker_compose) exec entities python3 -m sgqlc.introspection --exclude-deprecated --exclude-description http://localhost:8042/graphql api/schema.json
	$(docker_compose) exec entities sgqlc-codegen schema api/schema.json cli/gql_schema.py

### GitHub Actions ###################################################
.PHONY: gha-setup
gha-setup:
	docker swarm init

### ALEMBIC #############################################
alembic-upgrade-head:
	$(docker_compose) exec workflows alembic upgrade head ## Run alembic migrations locally

alembic-undo-migration: ## Downgrade the latest alembic migration
	$(docker_compose) exec workflows alembic downgrade -1

alembic-autogenerate: ## Create new alembic migrations files based on SA schema changes.
	$(docker_compose) exec workflows alembic revision --autogenerate -m "$(MESSAGE)" --rev-id $$(date +%Y%m%d_%H%M%S)

### SWIPE Plugin Tests

.PHONY: local-swipe-plugin-tests
local-swipe-plugin-start: local-envfile
	$(docker_compose) --profile moto --env-file .env.localdev up --force-recreate -d 

.PHONY: local-swipe-plugin-deploy-mock
local-swipe-plugin-deploy-mock: local-swipe-plugin-start
	- source environment.test; aws ssm put-parameter --name /mock-aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id --value ami-12345678 --type String --endpoint-url http://localhost:9000 --no-cli-pager
	source environment.test && \
	cd terraform_test && \
	find . -name '*tfstate*' | xargs rm -f && \
	unset TF_CLI_ARGS_init && \
	terraform init && \
	terraform apply --auto-approve

.PHONY: local-swipe-plugin-tests
local-swipe-plugin-tests: local-swipe-plugin-deploy-mock
	docker compose exec workflows sh -c 'pytest terraform_test/'

.PHONY: local-token
local-token: ## Copy an auth token for this local dev env to the system clipboard
	TOKEN=$$($(docker_compose) run entities ./cli/gqlcli.py auth generate-token 111 --project 444:admin --expiration 99999); echo '{"Authorization":"Bearer '$$TOKEN'"}' | tee >(pbcopy)
