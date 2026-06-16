"""Batch runner for multiple BLAKKBOX jobs.

Expected job layout:

jobs/customer_or_ecu_name/
├── original.bin
└── modified.bin
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(slots=True)
class BatchJob:
    name: str
    original: Path
    modified: Path
    output_dir: Path


class BatchRunner:
    def discover(self, job_root: str | Path, output_root: str | Path) -> list[BatchJob]:
        root = Path(job_root)
        out_root = Path(output_root)
        jobs: list[BatchJob] = []
        if not root.exists():
            raise FileNotFoundError(f"Job root not found: {root}")

        for folder in sorted(path for path in root.iterdir() if path.is_dir()):
            original_candidates = list(folder.glob("*ORIGINAL*.bin")) + list(folder.glob("original.bin"))
            modified_candidates = list(folder.glob("*MOD*.bin")) + list(folder.glob("modified.bin")) + list(folder.glob("mod.bin"))
            if not original_candidates or not modified_candidates:
                continue
            jobs.append(
                BatchJob(
                    name=folder.name,
                    original=original_candidates[0],
                    modified=modified_candidates[0],
                    output_dir=out_root / folder.name,
                )
            )
        return jobs

    def run(self, jobs: list[BatchJob], execute: Callable[[BatchJob], dict]) -> list[dict]:
        results: list[dict] = []
        for job in jobs:
            try:
                result = execute(job)
                results.append({"job": job.name, "status": "PASS", "result": result})
            except Exception as exc:  # pragma: no cover - used by CLI batch mode
                results.append({"job": job.name, "status": "FAIL", "error": str(exc)})
        return results
