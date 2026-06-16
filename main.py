"""BLAKKBOX command-line entry point."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Sequence

from batch.batch_runner import BatchJob, BatchRunner
from cli.args import parse_args
from core.logger import Logger, error, info
from core.workflow import Workflow


def _run_single(args) -> dict:
    workflow = Workflow()
    return workflow.run(
        original_file=str(args.original),
        modified_file=str(args.mod),
        output_dir=str(args.out),
        dry_run=bool(args.dry_run),
        strict=bool(args.strict),
        config_file=str(args.config) if args.config else None,
        protected_config=str(args.protected_config) if args.protected_config else None,
        write_markdown=not bool(args.no_markdown),
        write_manifest=not bool(args.no_manifest),
    )


def _run_batch(args) -> list[dict]:
    runner = BatchRunner()
    jobs = runner.discover(args.job_dir, args.out)
    if not jobs:
        raise RuntimeError(f"No valid jobs found in {args.job_dir}")

    workflow = Workflow()

    def execute(job: BatchJob) -> dict:
        info(f"Running batch job: {job.name}")
        return workflow.run(
            original_file=str(job.original),
            modified_file=str(job.modified),
            output_dir=str(job.output_dir),
            dry_run=bool(args.dry_run),
            strict=bool(args.strict),
            config_file=str(args.config) if args.config else None,
            protected_config=str(args.protected_config) if args.protected_config else None,
            write_markdown=not bool(args.no_markdown),
            write_manifest=not bool(args.no_manifest),
        )

    results = runner.run(jobs, execute)
    Path(args.out).mkdir(parents=True, exist_ok=True)
    (Path(args.out) / "batch_summary.json").write_text(
        json.dumps(results, indent=2, sort_keys=True), encoding="utf-8"
    )
    failures = [result for result in results if result["status"] != "PASS"]
    if failures:
        raise RuntimeError(f"{len(failures)} batch job(s) failed. See batch_summary.json")
    return results


def main(argv: Sequence[str] | None = None) -> int:
    Logger.configure()
    args = parse_args(argv)

    info("=" * 60)
    info("BLAKKBOX DENSO STUDIO v2")
    info("=" * 60)

    try:
        if args.job_dir:
            _run_batch(args)
        else:
            _run_single(args)
        info("=" * 60)
        info("Workflow Finished")
        info("=" * 60)
        return 0
    except KeyboardInterrupt:
        error("Execution cancelled by user.")
        return 1
    except Exception as exc:  # pragma: no cover - safety net for CLI users
        error("=" * 60)
        error("Unhandled Exception")
        error("=" * 60)
        error(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
