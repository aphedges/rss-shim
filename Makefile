.PHONY: default
default:
	@echo "an explicit target is required"

SHELL=/usr/bin/env bash

PYTHON_FILES=$(shell git ls-files '*.py' | sort | tr '\n' ' ')

.PHONY: black
black:
	pre-commit run --all-files black

.PHONY: codespell
codespell:
	pre-commit run --all-files codespell

.PHONY: flake8
flake8:
	pre-commit run --all-files flake8

.PHONY: isort
isort:
	pre-commit run --all-files isort

.PHONY: mypy
mypy:
	mypy $(PYTHON_FILES)

.PHONY: markdownlint
markdownlint:
	pre-commit run --all-files markdownlint

.PHONY: precommit
precommit:
	pre-commit run --all-files

.PHONY: prettier
prettier:
	pre-commit run --all-files prettier

.PHONY: pydocstyle
pydocstyle:
	pre-commit run --all-files pydocstyle

.PHONY: pylint
pylint:
	pylint $(PYTHON_FILES)

.PHONY: yamllint
yamllint:
	pre-commit run --all-files yamllint

.PHONY: check
check: precommit mypy pylint

.PHONY: install update
install update:
	pip install --upgrade pip setuptools wheel
	pip install --upgrade --upgrade-strategy eager -e .[dev]
