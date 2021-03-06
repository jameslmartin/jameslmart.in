.PHONY: help
.DEFAULT_GOAL := help

DOCKER_IMAGE=pelican:latest
APP_PORT=8000

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run-docker:
	@-docker rm -f $(DOCKER_CONTAINER_NAME)
	@docker run --rm \
		$(DOCKER_OPTS) \
		$(DOCKER_PORTS) \
 		--name=$(DOCKER_CONTAINER_NAME) \
		--workdir /home/app/ \
		$(DOCKER_IMAGE) $(DOCKER_CMD)

build-pelican: ## Build the latest pelican image
	docker build -t pelican -f ./Dockerfile .

dev: DOCKER_CONTAINER_NAME=pelican
dev: DOCKER_OPTS=-it -v `pwd`:/home/app/ \
	-v `pwd`/../pelican-themes:/home/themes \
	-v `pwd`/../pelican-plugins:/home/plugins \
	--workdir /app/
dev: DOCKER_PORTS=-p $(APP_PORT):8000
dev: DOCKER_CMD=bash
dev: run-docker
dev: ## Run Docker image for Pelican to generate local content

regen: DOCKER_CONTAINER_NAME=pelican
regen: DOCKER_OPTS=-t -v `pwd`:/home/app/ \
	-v `pwd`/../pelican-themes:/home/themes \
	-v `pwd`/../pelican-plugins:/home/plugins \
	--workdir /app/
regen: DOCKER_CMD=pelican /home/app/source/content -o /home/app/public -s /home/app/pelicanconf.py
regen: run-docker
regen: ## Just regen files


serve: ## Serve blog with livereload, to be run in the Docker container
	pelican -lr /home/app/source/content -o /home/app/public -s /home/app/pelicanconf.py -p 8000 -b 0.0.0.0
