"""Coordinates report building and JSON export."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.logger import info, kv, section
from export.json_exporter import JsonExporter
from export.metadata import MetadataBuilder


class ReportExporter:
    """Build and export the final analysis report."""

    def __init__(self) -> None:
        self.metadata = MetadataBuilder()
        self.json = JsonExporter()

    @staticmethod
    def _region_to_dict(region: Any) -> dict[str, Any]:
        return {
            "start": int(getattr(region, "start", 0)),
            "end": int(getattr(region, "end", 0)),
            "length": int(getattr(region, "length", 0)),
            "region_type": getattr(region, "region_type", "UNKNOWN"),
            "confidence": float(getattr(region, "confidence", 0.0)),
            "calibration": bool(getattr(region, "calibration", False)),
        }

    @staticmethod
    def _candidate_to_dict(candidate: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in candidate.items():
            if key == "region":
                continue
            result[key] = list(value) if isinstance(value, tuple) else value

        region = candidate.get("region")
        if region is not None:
            result["region"] = ReportExporter._region_to_dict(region)
        return result

    def build_report(
        self,
        original_file: str,
        modified_file: str,
        original_size: int,
        modified_size: int,
        fingerprint: dict[str, Any],
        delta_summary: dict[str, Any],
        regions: list[Any],
        classification_summary: dict[str, Any],
        axis_summary: dict[str, Any],
        axis_candidates: list[dict[str, Any]],
        geometry_summary: dict[str, Any],
        geometry_candidates: list[dict[str, Any]],
        filtered_delta_summary: dict[str, Any] | None = None,
        final_validation: dict[str, Any] | None = None,
        protected_hits: list[dict[str, Any]] | None = None,
        input_security: dict[str, Any] | None = None,
        output_bin: str | None = None,
    ) -> dict[str, Any]:
        report = self.metadata.build(
            original_file=original_file,
            modified_file=modified_file,
            original_size=original_size,
            modified_size=modified_size,
        )
        report["validation"] = {
            "rom_size_match": original_size == modified_size,
            "final_validation": final_validation or {},
            "protected_region_hits": protected_hits or [],
            "input_security": input_security or {},
        }
        report["fingerprint"] = fingerprint
        report["delta"] = {
            "summary": delta_summary,
            "regions": [self._region_to_dict(region) for region in regions],
            "filtered_delta": filtered_delta_summary or {},
        }
        report["classification"] = classification_summary
        report["axis"] = {
            "summary": axis_summary,
            "candidates": [
                self._candidate_to_dict(candidate) for candidate in axis_candidates
            ],
        }
        report["geometry"] = {
            "summary": geometry_summary,
            "tables": [
                self._candidate_to_dict(candidate) for candidate in geometry_candidates
            ],
        }
        report["final"] = {
            "formula": "ENHANCED_BIN = ORIGINAL_BIN + FILTERED_DELTA",
            "output_bin": output_bin,
        }
        return report

    def export(
        self,
        output_dir: str,
        original_file: str,
        modified_file: str,
        original_size: int,
        modified_size: int,
        fingerprint: dict[str, Any],
        delta_summary: dict[str, Any],
        regions: list[Any],
        classification_summary: dict[str, Any],
        axis_summary: dict[str, Any],
        axis_candidates: list[dict[str, Any]],
        geometry_summary: dict[str, Any],
        geometry_candidates: list[dict[str, Any]],
        filtered_delta_summary: dict[str, Any] | None = None,
        final_validation: dict[str, Any] | None = None,
        protected_hits: list[dict[str, Any]] | None = None,
        input_security: dict[str, Any] | None = None,
        output_bin: str | None = None,
        json_name: str = "analysis.json",
    ) -> Path:
        report = self.build_report(
            original_file=original_file,
            modified_file=modified_file,
            original_size=original_size,
            modified_size=modified_size,
            fingerprint=fingerprint,
            delta_summary=delta_summary,
            regions=regions,
            classification_summary=classification_summary,
            axis_summary=axis_summary,
            axis_candidates=axis_candidates,
            geometry_summary=geometry_summary,
            geometry_candidates=geometry_candidates,
            filtered_delta_summary=filtered_delta_summary,
            final_validation=final_validation,
            protected_hits=protected_hits,
            input_security=input_security,
            output_bin=output_bin,
        )

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        json_file = output_path / json_name
        self.json.export(output_file=str(json_file), report=report)

        section("EXPORT")
        kv("Report", str(json_file))
        if output_bin:
            kv("Enhanced BIN", output_bin)
        kv("Format", "JSON")
        info("Report export complete.")
        return json_file
