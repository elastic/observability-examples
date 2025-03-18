SHELL := bash

.PHONY: all
all: lint

.PHONY: lint
lint: markdown-link-check pre-commit

.PHONY: markdown-link-check
markdown-link-check:
	docker run --rm \
		--mount 'type=bind,source=$(PWD),target=/home/repo' \
		--workdir /home/repo \
		lycheeverse/lychee .

.PHONY: pre-commit
pre-commit:
	pre-commit run -a

.PHONY: lint-fix
lint-fix:
	ruff check --fix
