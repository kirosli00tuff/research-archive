.PHONY: install lint fmt typecheck test all guards mutations

install:
	uv sync

lint:
	uv run ruff format --check src tests
	uv run ruff check src tests

fmt:
	uv run ruff format src tests
	uv run ruff check --fix src tests

typecheck:
	uv run mypy

test:
	uv run pytest

all: lint typecheck test

guards:
	uv run pytest tests/test_guards.py tests/test_blindness.py -q

mutations:
	uv run python scripts/mutations.py
