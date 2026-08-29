.PHONY: help install lint typecheck test tables check clean

help: ## List available targets
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

install: ## Sync the Python environment (uv)
	uv sync --group dev

lint: ## Ruff format check + lint
	uv run ruff format --check .
	uv run ruff check .

typecheck: ## Mypy --strict over rplimits/ and tests/
	uv run mypy

test: ## Run the pytest suite (includes the honesty and drift tests)
	uv run pytest

tables: ## Print the generated evidence, contrast and sources tables
	uv run python -m rplimits

check: lint typecheck test ## The full gate

clean: ## Remove caches (never touches docs/)
	rm -rf .pytest_cache .mypy_cache .ruff_cache
