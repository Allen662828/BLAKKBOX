"""Command-line arguments for BLAKKBOX.

This replaces the old hardcoded ORIGINAL.bin / MOD.bin workflow with a
repeatable job-based interface and optional batch mode.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="blakkbox",
        description="OEM-preserving DENSO ROM enhancement pipeline",
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--original",
        type=Path,
        help="Path to the read-only ORIGINAL ROM file.",
    )
    input_group.add_argument(
        "--job-dir",
        type=Path,
        help="Batch job root. Each subfolder should contain original.bin and modified.bin/mod.bin.",
    )

    parser.add_argument(
        "--mod",
        type=Path,
        help="Path to the modified MOD ROM file. Required when --original is used.",
    )
    parser.add_argument(
        "--out",
        default=Path("output"),
        type=Path,
        help="Output folder for enhanced BIN and reports.",
    )
    parser.add_argument(
        "--config",
        default=None,
        type=Path,
        help="Optional pipeline YAML config. Defaults to configs/pipeline.yaml when present.",
    )
    parser.add_argument(
        "--protected-config",
        default=Path("configs/protected_regions.yaml"),
        type=Path,
        help="Optional protected-region YAML config. Missing file is allowed.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run analysis and validation without exporting enhanced.bin.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on any validation warning that may affect ROM integrity.",
    )
    parser.add_argument(
        "--no-markdown",
        action="store_true",
        help="Do not export analysis.md.",
    )
    parser.add_argument(
        "--no-manifest",
        action="store_true",
        help="Do not export manifest.json.",
    )

    args = parser.parse_args(argv)
    if args.original is not None and args.mod is None:
        parser.error("--mod is required when --original is used")
    if args.job_dir is not None and args.mod is not None:
        parser.error("--mod is only valid with --original, not --job-dir")
    return args
