from loader.rom_loader import RomLoader
from validation.validator import Validator
from fingerprint.fingerprint import FingerprintEngine
from delta.delta_engine import DeltaEngine

from classification.classifier import RegionClassifier
from classification.report import ClassificationReport

from axis.detector import AxisDetector
from geometry.detector import GeometryDetector


class Pipeline:
    """
    Generic Binary Analysis Pipeline

        Load
          │
        Validation
          │
        Fingerprint
          │
        Delta Analysis
          │
        Region Classification
          │
        Structural Analysis
          │
        Geometry Analysis
          │
        Report
    """

    def __init__(self):

        self.loader = RomLoader()
        self.validator = Validator()
        self.fingerprint = FingerprintEngine()

        self.delta = DeltaEngine()

        self.classifier = RegionClassifier()
        self.classification_report = ClassificationReport()

        self.axis = AxisDetector()
        self.geometry = GeometryDetector()

    def execute(self, original_file: str, modified_file: str):

        print("\nLoading files...\n")

        original, modified = self.loader.load(
            original_file,
            modified_file
        )

        self.validator.validate(
            original,
            modified
        )

        self.fingerprint.analyze(
            original
        )

        regions = self.delta.analyze(
            original,
            modified
        )

        regions = self.classifier.classify(
            regions
        )

        self.classification_report.print(
            regions
        )

        structural_candidates = self.axis.analyze(
            original,
            regions
        )

        structural_candidates = [
            c for c in structural_candidates
            if c.get("valid", False)
        ]

        geometry_candidates = self.geometry.analyze(
            structural_candidates
        )

        print()
        print("=" * 60)
        print("PIPELINE SUMMARY")
        print("=" * 60)

        print(f"Original Size        : {len(original):,} bytes")
        print(f"Modified Size        : {len(modified):,} bytes")
        print(f"Modified Regions     : {len(regions)}")
        print(f"Structural Candidates: {len(structural_candidates)}")
        print(f"Geometry Candidates  : {len(geometry_candidates)}")

        print("=" * 60)
        print("Analysis Complete")
        print("=" * 60)

        return {
            "regions": regions,
            "structures": structural_candidates,
            "geometry": geometry_candidates,
        }
