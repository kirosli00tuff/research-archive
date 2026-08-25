# Progress

Append-only. Newest at top. Each stage states its ETA before it starts and its
actual after it finishes.

---

## A.2. Binding registration. 2026-08-25

**ETA stated before start: 40 minutes. Actual: 34 minutes.**

A.2.0 ran first and gated everything downstream.

**Verified.** `gpt-5-2025-08-07` carries a knowledge cutoff of **2024-09-30**.
The served page reads `Sep 30, 2024 knowledge cutoff` verbatim. Source
https://developers.openai.com/api/docs/models/gpt-5, reached by 301 redirect
from platform.openai.com/docs/models/gpt-5, retrieved 2026-08-25. The same page
lists the snapshot `gpt-5-2025-08-07`, a 400,000 token context window, 128,000
max output tokens, and list prices of 1.25, 0.125, and 10.00 USD per million
for input, cached input, and output.

**The carried estimate was wrong.** Prior chat estimated 2024-05-31 and 515
days. The verified cutoff is four months later. The estimate is discarded.

**Derived.** Guard band of one calendar month ends 2024-10-30. Window runs
2024-10-31 through 2026-07-24. **432 trading days** from the source store's
own exchange calendar. The registered minimum is 200. The window clears it.

**Power.** Registered floor MDE 0.01787 against a floor of 0.025, so the window
is authorized. The primary contrast is weaker than the floor suggests: the
five-session horizon inflates variance by 3.4, cutting 427 evaluable days to
125.6 effective, and the minimum detectable contrast lands between 0.026 and
0.047. Registered as a limitation rather than repaired by swapping the primary.
ADR-007.

REGISTRATION.md written in full, 17 sections. Amendment 0 reserved and empty.
Assistant prior 0.05 recorded beside it.

---

## A.1. Scaffold. 2026-08-25

**ETA stated before start: 25 minutes. Actual: 22 minutes.**

Repository created at `~/Documents/GitHub/NPDExperiment`. `.env` was already
present at mode 600 and was never read, printed, or logged. `.gitignore`
covers it and `git check-ignore` confirms the match before the first commit.

Tooling: uv, ruff, mypy strict, pytest, pre-commit, Makefile.

Written: CLAUDE.md, DECISIONS.md with ADR-001 through ADR-007, progress.md,
REGISTRATION.md, `.env.example` carrying `OPENAI_API_KEY` commented and
valueless.

The two standing rules landed as code rather than prose. `npd.absence` makes
absence a type that refuses coercion to a number. `npd.callstate` holds the
five states and the classification that keeps them apart. `npd.config` holds
the frozen registered parameters, and every field in it needs an enforcement
site elsewhere or the structural guard fails.

Section 0's outcome map is committed in `npd.section0` and in REGISTRATION.md
Section 0. Both append-only ledgers exist, JSON lines, fsynced per row, and
they survive restart.
