.PHONY: help install lint typecheck test verify clean

help: ## List available targets
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

install: ## Sync the Python environment (uv) and install pre-commit hooks
	uv sync --group dev
	uv run pre-commit install

lint: ## Ruff format check + lint
	uv run ruff format --check .
	uv run ruff check .

typecheck: ## Mypy --strict over pmexperiment/ and tests/
	uv run mypy

test: ## Run the pytest suite (includes the honesty and registration tests)
	uv run pytest

verify: ## Report the recorded access state (Stage A fired PENDING_ACCESS)
	@echo "Stage A access gate fired PENDING_ACCESS on 2026-08-29."
	@echo "Recorded terms do not sanction keyless systematic retrieval;"
	@echo "re-probing is an operator decision. See docs/ACCESS.md and"
	@echo "DECISIONS.md ADR-006/ADR-007 before sending any request."

clean: ## Remove caches
	rm -rf .mypy_cache .ruff_cache .pytest_cache
