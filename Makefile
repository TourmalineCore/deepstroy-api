# If the first argument is "poetry"...
ifeq (poetry,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "poetry"
  POETRY_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(POETRY_ARGS):;@true)
endif

# If the first argument is "poetry-install"...
ifeq (poetry-install,$(firstword $(MAKECMDGOALS)))
ifeq ($(words $(MAKECMDGOALS)),3)
  # use the rest as arguments for "poetry-install"
  $(info $(MAKECMDGOALS))
  POETRY_INSTALL_PACKAGE_NAME := $(word 2,$(MAKECMDGOALS))
  POETRY_INSTALL_PACKAGE_VERSION := $(word 3,$(MAKECMDGOALS))

  POETRY_INSTALL_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(POETRY_INSTALL_ARGS):;@true)
else
  $(error poetry-install needs 2 arguments. See help)
endif
endif

# If the first argument is "poetry-install-dev"...
ifeq (poetry-install-dev,$(firstword $(MAKECMDGOALS)))
ifeq ($(words $(MAKECMDGOALS)),3)
  # use the rest as arguments for "poetry-install"
  $(info $(MAKECMDGOALS))
  POETRY_INSTALL_PACKAGE_NAME := $(word 2,$(MAKECMDGOALS))
  POETRY_INSTALL_PACKAGE_VERSION := $(word 3,$(MAKECMDGOALS))

  POETRY_INSTALL_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(POETRY_INSTALL_ARGS):;@true)
else
  $(error poetry-install-dev needs 2 arguments. See help)
endif
endif

# If the first argument is "create-migration"...
ifeq (create-migration,$(firstword $(MAKECMDGOALS)))
ifeq ($(words $(MAKECMDGOALS)),2)
  # use the rest as arguments for "create-migration"
  $(info $(MAKECMDGOALS))
  MIGRATION_NAME := $(word 2,$(MAKECMDGOALS))

  ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(ARGS):;@true)
else
  $(error create-migration needs 1 argument. See help)
endif
endif

# help
###
.PHONY: help
help: ;@true
	$(info Makefile for Tourmanique project)
	$(info )
	$(info Avaliable targets: )
	$(info  * install-local-deps                        - installs all dependencies from poetry.lock to have helpers for code locally)
	$(info  * lint                                      - runs linting)
	$(info  -- next will be executed via docker --)
	$(info  * poetry                                    - executes poetry command in the **docker** container)
	$(info  * poetry-install <package> <version>        - installs package in the **docker** container)
	$(info  * run                                       - runs the api locally via **docker**)
	$(info  * test                                      - runs unit tests via **docker**)
	$(info  * create-migration <migration_name>         - create migration with <migration_name> via **docker**)
	$(info )
	$(info Makefile: feel free to extend me!)

.PHONY: install-local-deps
install-local-deps: ## installs all dependencies from poetry.lock to have helpers for code locally
	poetry install

.PHONY: lint
lint: ## runs linting
	poetry run pylint \
	--load-plugins pylint_flask \
	--load-plugins pylint_flask_sqlalchemy \
	--generated-members=Column \
	--output-format=colorized \
	application.py tourmanique || poetry run pylint-exit $$?

.PHONY: poetry
poetry: ## executes poetry command in the docker container
	@echo poetry $(POETRY_ARGS)
	docker compose run --rm --no-deps tourmanique-api poetry $(POETRY_ARGS)

.PHONY: poetry-install
poetry-install: ## installs package in the **docker** container
	docker compose -f docker-compose.yml -f docker-compose.local.yml build --quiet tourmanique-api
	docker compose -f docker-compose.yml -f docker-compose.local.yml run --rm --no-deps tourmanique-api poetry add $(POETRY_INSTALL_PACKAGE_NAME) $(POETRY_INSTALL_PACKAGE_VERSION)

.PHONY: run
run: ## runs the api locally via **docker**
	docker compose -f docker-compose.yml -f docker-compose.local.yml up --build run-api-locally

.PHONY: test
test: ## runs unit tests via **docker**
	docker compose -f docker-compose.yml -f docker-compose.local.yml run --rm tourmanique-api poetry run pytest -v

.PHONY: create-migration
create-migration: ## create migration with <migration_name> via **docker**
	docker compose -f docker-compose.yml -f docker-compose.local.yml run --rm --no-deps tourmanique-api poetry run flask db migrate -m "$(MIGRATION_NAME)"