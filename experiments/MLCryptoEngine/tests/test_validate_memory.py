"""Memory regression guard: validation must process a large day in bounded RSS.

The 2026-07-31 full-day validation was OOM-killed at 12.8 GB RSS because the
replay retained every emitted snapshot row in memory before writing. The
validator had only ever been exercised on a 25-second fixture, three orders of
magnitude below a real day — exactly the gap this test closes. It generates a
synthetic venue-day large enough to force multiple streaming flushes, replays
it through the real ``validate_venue_day`` in a subprocess, and asserts the
subprocess's peak RSS stays under a fixed ceiling. Unbounded row retention at
this scale costs well over 1 GB and fails the ceiling; the streaming path
stays comfortably below it.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import orjson
import pyarrow.parquet as pq

from data.config import REPO_ROOT
from data.recorder.writer import RawFileWriter
from data.store import book_partition_dir

DATE = "2026-07-30"
# 2026-07-30T12:00:00Z — every synthetic message lands inside DATE.
BASE_NS = 1_785_412_800 * 1_000_000_000
MSG_SPACING_NS = 3_000_000  # 3 ms between messages ≈ 25 minutes of feed
SYMBOL = "BTC-USD"
DEPTH = 10

# Large enough that retaining every row in memory (~2.3 KB per emitted row,
# measured on real 2026-07-31 data) exceeds 1 GB, while the streaming path
# stays under the ceiling with wide margin.
N_MESSAGES = 400_000
PEAK_RSS_CEILING_MB = 600

# Runs inside the subprocess so peak memory is attributable to the validation
# alone. Prints machine-readable lines the test parses.
#
# **Read VmHWM, never ru_maxrss.** `getrusage(RUSAGE_SELF).ru_maxrss` is
# per-*process*, and Linux's `exec_mmap()` folds the pre-exec mm's high-water
# RSS into `signal->maxrss` — so a child forked from pytest inherits pytest's
# RSS as its own reported peak. Measured on this host: a child that allocates
# nothing reports 713 MB when its parent holds 700 MB at fork time. That made
# this guard report the *parent's* memory: it passed when run alone (small
# pytest) and failed inside the full suite (large pytest), while telling us
# nothing either way about the replay path. `/proc/self/status` VmHWM reads
# `mm->hiwater_rss` of the current mm, which execve resets, and stays at 13 MB
# in the same probe. See ADR-066.
DRIVER = """
import sys
from pathlib import Path

from data.config import AppConfig, load_config
from data.validate.replay import validate_venue_day

def _peak_rss_kb() -> int:
    for line in Path("/proc/self/status").read_text().splitlines():
        if line.startswith("VmHWM:"):
            return int(line.split()[1])
    raise RuntimeError("VmHWM absent from /proc/self/status; cannot measure peak RSS")

data_root = Path(sys.argv[1])
cfg = AppConfig(data_root=data_root, logs_dir=data_root / "logs", venues=load_config().venues)
report = validate_venue_day(cfg, "coinbase", sys.argv[2])

print(f"PEAK_RSS_KB={_peak_rss_kb()}")
print(f"MSGS={report.msgs_total}")
print(f"ROWS={sum(s.rows_written for s in report.symbols)}")
print(f"SEQ_GAPS={sum(s.seq_gaps or 0 for s in report.symbols)}")
print(f"CROSSED={sum(s.crossed_total for s in report.symbols)}")
"""


def _snapshot_message() -> dict[str, object]:
    updates = [
        {"side": "bid", "price_level": f"{50_000 - i}.0", "new_quantity": "1.0"}
        for i in range(DEPTH)
    ] + [
        {"side": "offer", "price_level": f"{50_001 + i}.0", "new_quantity": "1.0"}
        for i in range(DEPTH)
    ]
    return {
        "channel": "l2_data",
        "sequence_num": 0,
        "events": [{"type": "snapshot", "product_id": SYMBOL, "updates": updates}],
    }


def _update_message(seq: int) -> dict[str, object]:
    """One-level qty change that never removes a level and never crosses."""
    if seq % 2 == 0:
        side, price = "bid", 50_000 - (seq % 5)
    else:
        side, price = "offer", 50_001 + (seq % 5)
    update = {
        "side": side,
        "price_level": f"{price}.0",
        "new_quantity": f"{1 + (seq % 3)}.0",
    }
    return {
        "channel": "l2_data",
        "sequence_num": seq,
        "events": [{"type": "update", "product_id": SYMBOL, "updates": [update]}],
    }


def _generate_day(raw_dir: Path) -> None:
    writer = RawFileWriter(raw_dir, "coinbase")
    try:
        writer.write(BASE_NS, orjson.dumps(_snapshot_message()).decode())
        for seq in range(1, N_MESSAGES):
            writer.write(
                BASE_NS + seq * MSG_SPACING_NS, orjson.dumps(_update_message(seq)).decode()
            )
    finally:
        writer.close()


def test_validation_peak_rss_is_bounded_on_a_large_day(tmp_path: Path) -> None:
    # Arrange: a synthetic sequence-contiguous coinbase day, big enough that
    # retaining rows in memory would blow the ceiling several times over.
    _generate_day(tmp_path / "raw")

    # Act: validate in a subprocess so peak RSS is attributable to this run.
    result = subprocess.run(
        [sys.executable, "-c", DRIVER, str(tmp_path), DATE],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )

    # Assert: completed, processed everything, and stayed under the ceiling.
    assert result.returncode == 0, f"validation subprocess failed:\n{result.stderr[-2000:]}"
    values = dict(
        line.split("=", 1)
        for line in result.stdout.splitlines()
        if "=" in line and line.split("=", 1)[0].isupper()
    )
    assert int(values["MSGS"]) == N_MESSAGES
    assert int(values["SEQ_GAPS"]) == 0, "synthetic day is sequence-contiguous by construction"
    assert int(values["CROSSED"]) == 0, "synthetic updates never cross the book"

    rows_written = int(values["ROWS"])
    assert rows_written >= N_MESSAGES, "every l2 message must emit at least its event row"

    # The streamed parquet output must be complete and ordered, not just small.
    part = book_partition_dir(tmp_path / "processed", "coinbase", SYMBOL, DATE)
    table = pq.read_table(part / "part-000.parquet")
    assert table.num_rows == rows_written
    ts = table.column("ts_ns").to_pylist()
    assert ts == sorted(ts)

    peak_mb = int(values["PEAK_RSS_KB"]) / 1024
    assert peak_mb < PEAK_RSS_CEILING_MB, (
        f"validation peaked at {peak_mb:.0f} MB RSS for {N_MESSAGES:,} messages "
        f"(ceiling {PEAK_RSS_CEILING_MB} MB) — the replay path is retaining "
        "per-message state instead of streaming"
    )


def test_the_peak_rss_measurement_is_not_contaminated_by_this_process() -> None:
    """The guard above is only meaningful if it measures the child, not pytest.

    This is the defect that made the guard useless: ``ru_maxrss`` is
    per-process and Linux folds the pre-exec mm's high-water RSS into it, so a
    child forked from a large parent reports the parent's memory as its own
    peak. The guard therefore tracked pytest's footprint — passing alone and
    failing in the full suite — while saying nothing about the replay path, and
    it would have *masked* a real regression smaller than pytest itself.

    Asserting the two readings diverge under a fat parent is what stops a
    future edit from quietly reverting to ``ru_maxrss``.
    """
    # Arrange — a child that allocates essentially nothing, reporting both.
    probe = (
        "import resource, pathlib;"
        "hwm = next(l for l in pathlib.Path('/proc/self/status').read_text().splitlines()"
        " if l.startswith('VmHWM:')).split()[1];"
        "print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, hwm)"
    )
    ballast_mb = 400
    ballast = bytearray(ballast_mb * 1024 * 1024)
    for offset in range(0, len(ballast), 4096):  # touch it, so it is resident
        ballast[offset] = 1

    # Act — fork/exec from this deliberately fat parent.
    try:
        result = subprocess.run(
            [sys.executable, "-c", probe], capture_output=True, text=True, check=True
        )
        ru_maxrss_kb, vmhwm_kb = (int(v) for v in result.stdout.split())
    finally:
        del ballast

    # Assert — the child allocated nothing, so an honest reading must be small.
    assert vmhwm_kb / 1024 < 100, (
        f"VmHWM read {vmhwm_kb / 1024:.0f} MB for a child that allocates nothing; "
        "the measurement the guard relies on is no longer clean"
    )
    # And the discredited reading must visibly carry the parent's memory, or
    # this test is asserting a distinction that has stopped existing.
    assert ru_maxrss_kb / 1024 > ballast_mb, (
        f"ru_maxrss read {ru_maxrss_kb / 1024:.0f} MB from a parent holding "
        f"{ballast_mb} MB — the contamination this guard works around appears to "
        "be gone; re-derive the measurement choice before simplifying it away"
    )
