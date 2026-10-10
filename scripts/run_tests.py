"""Convenience runner: python scripts/run_tests.py"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
report_dir = ROOT / "reports"
report_dir.mkdir(exist_ok=True)
cmd = [
    sys.executable, "-m", "pytest", "-v",
    f"--html={report_dir / 'pytest-report.html'}",
    "--self-contained-html",
]
raise SystemExit(subprocess.call(cmd, cwd=ROOT))
