"""
export/metadata.py

Metadata builder for exported analysis reports.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


class MetadataBuilder:
    """
    Builds metadata describing the analysis session.
    """

    def build(
        self,
        original_file: str,
        modified_file: str,
        original_size: int,
        modified_size: int,
    ) -> dict[str, Any]:

        original = Path(original_file)
        modified = Path(modified_file)

        return {
            "project": "BLAKKBOX",
            "version": "0.4.0-dev",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "original": {
                "filename": original.name,
                "size": original_size,
            },
            "modified": {
                "filename": modified.name,
                "size": modified_size,
            },
        }
