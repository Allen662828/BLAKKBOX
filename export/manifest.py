"""Job manifest export for traceable BLAKKBOX runs."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class ManifestExporter:
    def build(
        self,
        *,
        original_file: str | Path,
        modified_file: str | Path,
        output_bin: str | Path | None,
        report_file: str | Path | None,
        status: str,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        original = Path(original_file)
        modified = Path(modified_file)
        manifest: dict[str, Any] = {
            "tool": "BLAKKBOX",
            "version": "v2",
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "formula": "ENHANCED_BIN = ORIGINAL_BIN + FILTERED_DELTA",
            "status": status,
            "inputs": {
                "original": {
                    "path": str(original),
                    "size": original.stat().st_size if original.exists() else None,
                    "sha256": sha256_file(original) if original.exists() else None,
                },
                "modified": {
                    "path": str(modified),
                    "size": modified.stat().st_size if modified.exists() else None,
                    "sha256": sha256_file(modified) if modified.exists() else None,
                },
            },
            "outputs": {
                "enhanced_bin": str(output_bin) if output_bin else None,
                "analysis_report": str(report_file) if report_file else None,
            },
        }
        if output_bin and Path(output_bin).exists():
            manifest["outputs"]["enhanced_sha256"] = sha256_file(output_bin)
            manifest["outputs"]["enhanced_size"] = Path(output_bin).stat().st_size
        if extra:
            manifest["extra"] = extra
        return manifest

    def export(self, output_file: str | Path, manifest: dict[str, Any]) -> Path:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        return path
