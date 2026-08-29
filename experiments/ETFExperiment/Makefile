SCRIPTS = scripts

.PHONY: install lint fmt typecheck test all guards mutations

install:
	uv sync

lint:
	uv run ruff format --check src tests $(SCRIPTS)
	uv run ruff check src tests $(SCRIPTS)

fmt:
	uv run ruff format src tests $(SCRIPTS)
	uv run ruff check --fix src tests $(SCRIPTS)

typecheck:
	uv run mypy

test:
	uv run pytest

all: lint typecheck test

guards:
	uv run pytest tests/test_guards.py tests/test_blindness.py tests/test_preperiod.py -q

mutations:
	uv run python scripts/mutations.py
