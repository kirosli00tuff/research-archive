SCRIPTS = scripts/mutations.py scripts/mutations_stage_b.py scripts/mutations_register.py \
          scripts/mutations_amend.py scripts/backfill_fallback.py scripts/ktable_amended.py \
          scripts/h5_census.py scripts/h5_retro.py \
          scripts/h5_pass.py scripts/h5_fire.py scripts/mutations_h5.py

.PHONY: install lint fmt typecheck test all guards \
        mutations mutations-b mutations-register mutations-amend \
        backfill-fallback ktable-amended h5-census h5-retro h5-pass h5-fire mutations-h5

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
	uv run pytest tests/test_guards.py tests/test_blindness.py -q

mutations:
	uv run python scripts/mutations.py

mutations-b:
	uv run python scripts/mutations_stage_b.py

mutations-register:
	uv run python scripts/mutations_register.py

mutations-amend:
	uv run python scripts/mutations_amend.py

backfill-fallback:
	uv run python scripts/backfill_fallback.py

ktable-amended:
	uv run python scripts/ktable_amended.py

h5-census:
	uv run python scripts/h5_census.py

h5-retro:
	uv run python scripts/h5_retro.py

h5-pass:
	uv run python scripts/h5_pass.py scripts/h5_fire.py scripts/mutations_h5.py

h5-fire:
	uv run python scripts/h5_fire.py scripts/mutations_h5.py

mutations-h5:
	uv run python scripts/mutations_h5.py
