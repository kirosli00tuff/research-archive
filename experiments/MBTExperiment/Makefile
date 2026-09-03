.PHONY: help install lint typecheck test guards no-transmit boundary all \
        b-probe b-probe-full b-straddle b-known-answer b-census b-whatif-live \
        b-gates mutations clean

help: ## List available targets
	@grep -E '^[a-z0-9-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-20s %s\n", $$1, $$2}'

install: ## Sync the environment (uv) and install pre-commit hooks
	uv sync --group dev
	uv run pre-commit install

lint: ## Ruff format check + lint
	uv run ruff format --check .
	uv run ruff check .

typecheck: ## Mypy --strict over src/mbt, tests and tools
	uv run mypy

test: ## Run the pytest suite (guards and honesty tests are load-bearing)
	uv run pytest

no-transmit: ## Guard one alone: the AST walk over the package's parse trees
	uv run python tools/no_transmit_scan.py --json reports/guards/no_transmit_scan.json

guards: no-transmit ## The five structural guards, plus the credential and account scan
	uv run pytest tests/test_guards.py tests/test_honesty.py -q

boundary: ## Hash the read-only VRPExperiment boundary. LABEL=open|close
	uv run python tools/boundary_hash.py \
		--root $$(uv run python tools/find_boundary.py) \
		--out reports/boundary/vrp_manifest_$(LABEL).txt \
		--json reports/boundary/vrp_boundary_$(LABEL).json \
		--label $(LABEL)

all: lint typecheck no-transmit test ## lint, typecheck, no-transmit scan, test

b-probe: ## PAPER. Connect, verify permission, record the environment provenance
	uv run python -m mbt.cli probe --env paper

b-probe-full: ## PAPER. Handshake, permission, subscription state on all three legs
	uv run python -m mbt.cli probe-full --env paper

b-straddle: ## PAPER. Resolve the registered ATM 30-day straddle from the live chain
	uv run python -m mbt.cli straddle --env paper

b-known-answer: ## PAPER. Reproduce a checkable margin through the MBT code path
	uv run python -m mbt.cli known-answer --env paper

b-census: ## PAPER. Append one bid-ask observation window; clock-bound to 20
	uv run python -m mbt.cli census --env paper

b-whatif-live: ## DISABLED. Paper-only clause is in force; see CLAUDE.md
	@echo "REFUSED: the paper-only clause is in force. The MARGIN gate is"
	@echo "Absent(no_live_session) and no live session runs from this repo."
	@echo "Lifting the clause is an operator edit to CLAUDE.md, never a flag."
	@exit 1

b-gates: ## Fire the MARGIN and COST gates, offline, from recorded figures
	uv run python -m mbt.cli gates

mutations: ## Apply the five registered mutations to real source and restore
	uv run python tools/mutations.py

clean: ## Remove caches (never touches data/ or reports/)
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} +
