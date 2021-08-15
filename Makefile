VOLUMES ?= 
PORTS ?= -p 8080:8080
ENV ?= 

IMAGE_REGISTRY ?= mrbarker
IMAGE_NAME ?= python-flask-hello
IMAGE_VERSION ?= latest

CONTAINER_NAME ?= pfhello
CONTAINER_INSTANCE ?= default

.PHONY: build push shell run start stop rm release 

build: Dockerfile
	docker build -t $(IMAGE_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION) -f Dockerfile .

push:
	docker push $(IMAGE_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION)
    
shell:
	docker run --rm --name $(CONTAINER_NAME)-$(CONTAINER_INSTANCE) -i -t $(PORTS) $(VOLUMES) $(ENV) $(IMAGE_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION) /bin/bash

run:
	docker run --rm --name $(CONTAINER_NAME)-$(CONTAINER_INSTANCE) $(PORTS) $(VOLUMES) $(ENV) $(IMAGE_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION)

start:
	docker run -d --name $(CONTAINER_NAME)-$(CONTAINER_INSTANCE) $(PORTS) $(VOLUMES) $(ENV) $(IMAGE_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION)

stop:
	docker stop $(CONTAINER_NAME)-$(CONTAINER_INSTANCE)

rm:
	docker rm $(CONTAINER_NAME)-$(CONTAINER_INSTANCE)

release: build
	make push -e IMAGE_VERSION=$(IMAGE_VERSION)
    
default: build
