.PHONY: docker-build docker-run build

USER := $(shell id -u)
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
VERSION := $(shell git describe --always --tags | grep -Eo "[0-9]+\.[0-9]+\.[0-9]+")

docker-build:
	docker build -t chengtian/spider163:$(VERSION) -f hack/spider/Dockerfile .

docker-run:
	cd hack && docker-compose up

build:
	pip install -e .


