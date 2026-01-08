.PHONY: welcome
welcome:
	@printf "\033c"
	@cat etc/make/welcome.mk
	@echo ''

.PHONY: build-env
## @Build Build environment configuration
build-env:
	@printf " - Build ${GREEN}.env${RESET} \n"
	$(shell cat etc/.env.dist > .env)
	$(shell echo "UID=$(UID)" >> .env)
	$(shell echo "GID=$(GID)" >> .env)
	$(shell echo "USER_NAME=$(USER_NAME)" >> .env)
	$(shell echo "LOCAL_USER=$(UID):$(GID)" >> .env)
	$(shell echo "PATH=$(PATH)" >> .env)
	$(shell echo "PWD=$(PWD)" >> .env)
	$(shell echo "PIP_CACHE_HOME=$(PIP_CACHE_HOME)" >> .env)
	$(shell echo "LOCAL_HOME=$(LOCAL_HOME)" >> .env)
	$(shell mkdir -p ${PIP_CACHE_HOME})
	$(shell mkdir -p ${LOCAL_HOME})

.PHONY: docker-build
## @Docker Build the image of the application
docker-build: build-env
	@docker compose build --force-rm ${CONTAINER_NAME}

.PHONY: docker-cli
## @Docker Connect in the application layer
docker-cli: build-env
	@bin/console bash

