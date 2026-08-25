.PHONY: install lint type test guards all b0 b0b b1 status clean

install:
	uv venv --python 3.11
	uv pip install -e ".[dev]"

lint:
	uv run ruff check src tests scripts
	uv run ruff format --check src tests scripts

type:
	uv run mypy

test:
	uv run pytest

guards:
	uv run pytest tests/test_guards.py -v

all: lint type test

b0:
	uv run python -m npd.data.build

b0b:
	uv run python -m npd.collect --adapter mock --scenarios all

b1:
	uv run python -m npd.collect --adapter openai

status:
	uv run python -m npd.collect --status

clean:
	uv run python scripts/clean_caches.py
