.PHONY: install lint fmt typecheck test all guards mutations mutations-b mutations-register

install:
	uv sync

lint:
	uv run ruff format --check src tests scripts/mutations.py scripts/mutations_stage_b.py scripts/mutations_register.py
	uv run ruff check src tests scripts/mutations.py scripts/mutations_stage_b.py scripts/mutations_register.py

fmt:
	uv run ruff format src tests scripts/mutations.py scripts/mutations_stage_b.py scripts/mutations_register.py
	uv run ruff check --fix src tests scripts/mutations.py scripts/mutations_stage_b.py scripts/mutations_register.py

typecheck:
	uv run mypy

test:
	uv run pytest

all: lint typecheck test

guards:
	uv run pytest tests/test_guards.py tests/test_blindness.py -q

mutations:
	uv run python scripts/mutations.py

mutations-b:
	uv run python scripts/mutations_stage_b.py

mutations-register:
	uv run python scripts/mutations_register.py
