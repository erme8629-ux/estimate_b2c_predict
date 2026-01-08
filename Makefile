MAKEFILE := $(abspath $(lastword $(MAKEFILE_LIST)))

# Load environment vars
include etc/.env.dist
export $(shell sed 's/=.*//' etc/.env.dist)

USER_NAME ?= $(shell id -u -n)
UID ?= $(shell id -u)
GID ?= $(shell id -g)
PWD ?= $(shell pwd)
PATH?=$(shell echo $PATH)
PIP_CACHE_HOME=$(PWD)/.cache/pip
LOCAL_HOME=$(PWD)/.local
INSTALL_DOCKER=which docker || sudo bin/docker-install

ifeq ($(shell uname -s),Darwin)
	OS=osx
else
	OS=linux
endif

ifneq ("$(wildcard .install)","")
    include .install
    export $(shell sed 's/=.*//' .install)
endif

include etc/make/help.mk
include etc/make/command.mk

