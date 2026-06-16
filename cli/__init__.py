# cli/args.py
from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="blakkbox",
        description="OEM-preserving DENSO ROM enhancement pipeline",
    )

    parser.add_argument("--original", required=True, type=Path)
    parser.add_argument("--mod", required=True, type=Path)
    parser.add_argument("--out", default=Path("output"), type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--strict", action="store_true")

    return parser.parse_args()