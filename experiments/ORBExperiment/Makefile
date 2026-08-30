.PHONY: install lint fmt typecheck test all guards mutations clean

VENV := .venv
PY   := $(VENV)/bin/python
PURGE := find . -name '__pycache__' -type d -prune -exec rm -rf {} +

install:
	uv venv --python 3.13 $(VENV) 2>/dev/null || uv venv $(VENV)
	uv pip install --python $(PY) -e ".[dev]"

fmt:
	$(VENV)/bin/ruff format src tests
	$(VENV)/bin/ruff check --fix src tests

lint:
	$(VENV)/bin/ruff format --check src tests
	$(VENV)/bin/ruff check src tests

typecheck:
	$(VENV)/bin/mypy

test:
	$(VENV)/bin/pytest

guards:
	$(VENV)/bin/pytest tests/test_guards.py -v

mutations:
	$(PURGE) 2>/dev/null || true
	$(PY) tools/mutate.py

all: lint typecheck test

clean:
	$(PURGE) 2>/dev/null || true
