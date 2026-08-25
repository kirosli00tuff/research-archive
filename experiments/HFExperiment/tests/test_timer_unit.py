"""The timer unit is valid and runs Mon to Fri at 23:30 UTC."""
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TIMER = ROOT / "systemd" / "hfexperiment-bars.timer"
SERVICE = ROOT / "systemd" / "hfexperiment-bars.service"
CALENDAR = "Mon..Fri *-*-* 23:30:00 UTC"


def test_timer_calendar_is_mon_to_fri_2330_utc() -> None:
    text = TIMER.read_text()
    assert f"OnCalendar={CALENDAR}" in text
    assert "Persistent=true" in text
    assert "WantedBy=timers.target" in text


def test_service_runs_daily_run_with_the_memory_cap() -> None:
    text = SERVICE.read_text()
    assert "Type=oneshot" in text
    assert "MemoryMax=2G" in text
    assert "daily_run.py" in text


@pytest.mark.skipif(
    shutil.which("systemd-analyze") is None,
    reason="systemd-analyze not available",
)
def test_calendar_expression_is_valid_and_elapses_at_2330_utc() -> None:
    proc = subprocess.run(
        ["systemd-analyze", "calendar", CALENDAR],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert proc.returncode == 0, proc.stderr
    assert "23:30:00 UTC" in proc.stdout
