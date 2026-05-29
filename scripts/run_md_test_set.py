"""Compatibility launcher for the batch MD benchmark workflow."""

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from iphasimulator.workflows.md_benchmark import main  # noqa: E402


if __name__ == "__main__":
    main()
