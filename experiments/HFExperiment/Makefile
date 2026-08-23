.PHONY: install lint type test check reproduce

install:
	uv sync

lint:
	uv run ruff check src tests scripts

type:
	uv run mypy

test:
	uv run pytest

check: lint type test

reproduce:
	uv run python scripts/reproduce_formation.py
