"""Human-readable markdown report export."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class MarkdownReportExporter:
    def build(self, report: dict[str, Any]) -> str:
        validation = report.get("validation", {})
        final_validation = validation.get("final_validation", {})
        delta = report.get("delta", {})
        filtered_delta = delta.get("filtered_delta", {})
        final = report.get("final", {})

        lines = [
            "# BLAKKBOX Enhancement Report",
            "",
            "## Final Formula",
            "",
            "```text",
            str(final.get("formula", "ENHANCED_BIN = ORIGINAL_BIN + FILTERED_DELTA")),
            "```",
            "",
            "## Validation",
            "",
        ]

        if final_validation:
            for key, value in final_validation.items():
                lines.append(f"- **{key}**: {value}")
        else:
            lines.append("- No final validation summary available.")

        lines.extend(["", "## Filtered Delta", ""])
        if filtered_delta:
            for key, value in filtered_delta.items():
                lines.append(f"- **{key}**: {value}")
        else:
            lines.append("- No filtered delta summary available.")

        lines.extend(["", "## Output", "", f"- Enhanced BIN: `{final.get('output_bin')}`"])
        return "\n".join(lines) + "\n"

    def export(self, output_file: str | Path, report: dict[str, Any]) -> Path:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.build(report), encoding="utf-8")
        return path
