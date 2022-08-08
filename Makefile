# Makefile for stilted

.DEFAULT_GOAL := help

.PHONY: check coverage flake help mypy size test

help:				## Display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

check: mypy flake test		## Make sure everything is good

flake:				## Run pyflakes to clean things up
	pyflakes *.py

mypy:				## Run mypy to check types
	mypy --check-untyped-defs *.py

test:				## Run the tests
	pytest -q -rfeX

coverage:			## Measure test coverage
	coverage run --branch --source=. -m pytest -q
	coverage report --skip-covered --show-missing --precision=2
	coverage html --skip-covered --precision=2

size:
	cloc -q --hide-rate *.py
	python cli.py -c "systemdict length =="
