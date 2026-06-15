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

from core.logger import (
    section,
    kv,
    info,
)


class Pipeline:
    """
    ==========================================================
                  BLAKKBOX Analysis Pipeline
    ==========================================================

        Load ROMs
              │
        Validation
              │
        ROM Fingerprint
              │
        Delta Analysis
              │
        Region Classification
              │
        Axis Analysis
              │
        Geometry Analysis
              │
        Pipeline Summary
    ==========================================================
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

    def execute(
        self,
        original_file: str,
        modified_file: str,
    ) -> dict:

        # ------------------------------------------------------
        # Load ROMs
        # ------------------------------------------------------

        original, modified = self.loader.load(
            original_file,
            modified_file,
        )

        # ------------------------------------------------------
        # Validation
        # ------------------------------------------------------

        self.validator.validate(
            original,
            modified,
        )

        # ------------------------------------------------------
        # Fingerprint
        # ------------------------------------------------------

        fingerprint = self.fingerprint.analyze(original)

        # ------------------------------------------------------
        # Delta Analysis
        # ------------------------------------------------------

        regions = self.delta.analyze(
            original,
            modified,
        )

        # ------------------------------------------------------
        # Region Classification
        # ------------------------------------------------------

        regions = self.classifier.classify(regions)

        classification_summary = self.classification_report.print(regions)

        # ------------------------------------------------------
        # Axis Analysis
        # ------------------------------------------------------

        axis_candidates = self.axis.analyze(
            original,
            regions,
        )

        valid_axis = [
            candidate
            for candidate in axis_candidates
            if candidate.get(
                "valid",
                False,
            )
        ]

        # ------------------------------------------------------
        # Geometry Analysis
        # ------------------------------------------------------

        geometry_candidates = self.geometry.analyze(valid_axis)

        valid_geometry = [
            table
            for table in geometry_candidates
            if table.get(
                "valid",
                False,
            )
        ]

        # ------------------------------------------------------
        # Pipeline Summary
        # ------------------------------------------------------

        section("PIPELINE SUMMARY")

        kv(
            "Original Size",
            f"{len(original):,} bytes",
        )

        kv(
            "Modified Size",
            f"{len(modified):,} bytes",
        )

        kv(
            "Modified Regions",
            len(regions),
        )

        kv(
            "Calibration Regions",
            classification_summary["calibration"],
        )

        kv(
            "Axis Candidates",
            len(axis_candidates),
        )

        kv(
            "Valid Axis",
            len(valid_axis),
        )

        kv(
            "Geometry Candidates",
            len(geometry_candidates),
        )

        kv(
            "Valid Geometry",
            len(valid_geometry),
        )

        info("")
        info("Analysis Complete")

        # ------------------------------------------------------
        # Return Results
        # ------------------------------------------------------

        return {
            "fingerprint": fingerprint,
            "regions": regions,
            "classification": classification_summary,
            "axis": axis_candidates,
            "valid_axis": valid_axis,
            "geometry": geometry_candidates,
            "valid_geometry": valid_geometry,
        }
