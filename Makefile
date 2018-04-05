.PHONY: docker-build composer build

USER := $(shell id -u)
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
VERSION := $(shell git describe --always --tags | grep -Eo "[0-9]+\.[0-9]+\.[0-9]+")

docker-build:
	docker build -t spider163:$(VERSION) -f hack/spider/Dockerfile .
	docker build -t mysql163:$(VERSION) -f hack/mysql/Dockerfile .

composer:
	docker-compose -p "spider163-$(BRANCH)-$(USER)" up

build:
	pip install -e .
