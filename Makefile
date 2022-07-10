# Makefile for stilted

.DEFAULT_GOAL := help

.PHONY: check help mypy test

help:				## Display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

check: mypy test		## Make sure everything is good

mypy:				## Run mypy to check types
	mypy *.py

test:				## Run the tests
	pytest -q
