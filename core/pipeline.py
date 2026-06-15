"""
core/pipeline.py

Main BLAKKBOX analysis pipeline.
"""

from __future__ import annotations

from loader.rom_loader import RomLoader
from validation.validator import Validator
from fingerprint.fingerprint import FingerprintEngine
from delta.delta_engine import DeltaEngine

from classification.classifier import RegionClassifier
from classification.report import ClassificationReport

from axis.detector import AxisDetector
from geometry.detector import GeometryDetector

from export.report_exporter import ReportExporter

from core.logger import section, kv, info


class Pipeline:
    """
    Main analysis pipeline.
    """

    def __init__(self) -> None:
        self.loader = RomLoader()
        self.validator = Validator()
        self.fingerprint = FingerprintEngine()
        self.delta = DeltaEngine()
        self.classifier = RegionClassifier()
        self.classification_report = ClassificationReport()
        self.axis = AxisDetector()
        self.geometry = GeometryDetector()
        self.report_exporter = ReportExporter()

    def execute(self, original_file: str, modified_file: str) -> dict:

        info("Loading files...")

        original, modified = self.loader.load(
            original_file,
            modified_file,
        )

        self.validator.validate(
            original,
            modified,
        )

        fingerprint = self.fingerprint.analyze(original)

        regions = self.delta.analyze(
            original,
            modified,
        )

        delta_summary = self.delta.statistics.summarize(regions)

        regions = self.classifier.classify(regions)

        classification_summary = self.classification_report.print(regions)

        axis_candidates = self.axis.analyze(
            original,
            regions,
        )

        valid_axis = [
            candidate
            for candidate in axis_candidates
            if candidate.get("valid", False)
        ]

        axis_summary = {
            "total": len(axis_candidates),
            "valid": len(valid_axis),
            "rejected": len(axis_candidates) - len(valid_axis),
        }

        geometry_candidates = self.geometry.analyze(valid_axis)

        valid_geometry = [
            candidate
            for candidate in geometry_candidates
            if candidate.get("valid", False)
        ]

        geometry_summary = {
            "total": len(geometry_candidates),
            "valid": len(valid_geometry),
            "rejected": len(geometry_candidates) - len(valid_geometry),
        }

        self.report_exporter.export(
            output_dir="output",
            original_file=original_file,
            modified_file=modified_file,
            original_size=len(original),
            modified_size=len(modified),
            fingerprint=fingerprint,
            delta_summary=delta_summary,
            regions=regions,
            classification_summary=classification_summary,
            axis_summary=axis_summary,
            axis_candidates=axis_candidates,
            geometry_summary=geometry_summary,
            geometry_candidates=geometry_candidates,
        )

        section("PIPELINE SUMMARY")
        kv("Original Size", f"{len(original):,} bytes")
        kv("Modified Size", f"{len(modified):,} bytes")
        kv("Modified Regions", len(regions))
        kv("Calibration Regions", classification_summary["calibration"])
        kv("Axis Candidates", axis_summary["total"])
        kv("Valid Axis", axis_summary["valid"])
        kv("Geometry Candidates", geometry_summary["total"])
        kv("Valid Geometry", geometry_summary["valid"])

        info("Analysis Complete")

        return {
            "fingerprint": fingerprint,
            "delta": delta_summary,
            "classification": classification_summary,
            "axis": axis_summary,
            "geometry": geometry_summary,
        }
