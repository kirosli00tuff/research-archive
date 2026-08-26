.PHONY: install lint fmt type test guards all a1-market a1-corpus a1-power mutations

install:
	uv venv --python 3.12
	uv pip install -e ".[dev]"

lint:
	uv run ruff check src tests scripts
	uv run ruff format --check src tests scripts

fmt:
	uv run ruff format src tests scripts
	uv run ruff check --fix src tests scripts

type:
	uv run mypy

test:
	uv run pytest

guards:
	uv run pytest tests/test_guards.py -v

all: lint type test

a1-market:
	uv run python -m insider.market.build

a1-corpus:
	uv run python -m insider.corpus.build

a1-power:
	uv run python -m insider.power.report

mutations:
	uv run python scripts/mutations.py
