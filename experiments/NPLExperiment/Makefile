.PHONY: install lint fmt typecheck test all guards mutations

install:
	uv sync

lint:
	uv run ruff format --check src tests scripts/mutations.py
	uv run ruff check src tests scripts/mutations.py

fmt:
	uv run ruff format src tests scripts/mutations.py
	uv run ruff check --fix src tests scripts/mutations.py

typecheck:
	uv run mypy

test:
	uv run pytest

all: lint typecheck test

guards:
	uv run pytest tests/test_guards.py tests/test_blindness.py -q

mutations:
	uv run python scripts/mutations.py
