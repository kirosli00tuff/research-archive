.PHONY: help install lint typecheck test guards all a1-probe a1-chain a1-whatif-paper a1-census a1-whatif-live a1-gates mutations clean

help: ## List available targets
	@grep -E '^[a-z0-9-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-20s %s\n", $$1, $$2}'

install: ## Sync the environment (uv) and install pre-commit hooks
	uv sync --group dev
	uv run pre-commit install

lint: ## Ruff format check + lint
	uv run ruff format --check .
	uv run ruff check .

typecheck: ## Mypy --strict over src/mbt and tests
	uv run mypy

test: ## Run the pytest suite (guards and honesty tests are load-bearing)
	uv run pytest

guards: ## The structural guards alone, including the no-transmit AST scan
	uv run pytest tests/test_guards.py -q

all: lint typecheck test ## lint, typecheck, test

a1-probe: ## PAPER. Connect, verify permission, record the environment provenance
	uv run python -m mbt.cli probe --env paper

a1-chain: ## PAPER. Resolve the ATM 30-day MBT straddle from the live chain
	uv run python -m mbt.cli chain --env paper

a1-whatif-paper: ## PAPER. Margin read for development only; never verdict-bearing
	uv run python -m mbt.cli whatif --env paper

a1-census: ## PAPER. Append one bid-ask observation window; clock-bound to 20
	uv run python -m mbt.cli census --env paper

a1-whatif-live: ## DISABLED. Paper-only clause is in force; see CLAUDE.md
	@echo "REFUSED: the paper-only clause is in force. The MARGIN gate is"
	@echo "Absent(no_live_session) and no live session runs from this repo."
	@echo "Lifting the clause is an operator edit to CLAUDE.md, never a flag."
	@exit 1

a1-gates: ## Fire the MARGIN and COST gates, offline, from recorded figures
	uv run python -m mbt.cli gates

mutations: ## Apply the registered mutations and restore
	uv run python -m mbt.cli mutations

clean: ## Remove caches (never touches data/ or var/)
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} +
