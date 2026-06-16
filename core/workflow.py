"""Top-level BLAKKBOX workflow wrapper."""

from __future__ import annotations

from core.pipeline import Pipeline


class Workflow:
    def __init__(self) -> None:
        self.pipeline = Pipeline()

    def run(
        self,
        original_file: str,
        modified_file: str,
        output_dir: str = "output",
        dry_run: bool = False,
        strict: bool = False,
        config_file: str | None = None,
        protected_config: str | None = None,
        write_markdown: bool = True,
        write_manifest: bool = True,
    ) -> dict:
        return self.pipeline.execute(
            original_file=original_file,
            modified_file=modified_file,
            output_dir=output_dir,
            dry_run=dry_run,
            strict=strict,
            config_file=config_file,
            protected_config=protected_config,
            write_markdown=write_markdown,
            write_manifest=write_manifest,
        )
