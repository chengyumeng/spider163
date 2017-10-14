.PHONY: docker-build composer build

USER := $(shell id -u)
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)


docker-build:
	docker build -t spider163 -f hack/spider/Dockerfile .
	docker build -t mysql163 -f hack/mysql/Dockerfile .

composer:
	docker-compose -p "spider163-$(BRANCH)-$(USER)" up

build:
	pip install -r requirements.txt
	python setup.py install
	python setup.py clean
