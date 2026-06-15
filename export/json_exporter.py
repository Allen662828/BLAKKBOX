"""
export/json_exporter.py

JSON report exporter.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonExporter:
    """
    Export analysis results as JSON.
    """

    def export(
        self,
        output_file: str,
        report: dict[str, Any],
    ) -> None:

        path = Path(output_file)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                report,
                fp,
                indent=4,
                sort_keys=True,
            )
