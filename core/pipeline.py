from loader.rom_loader import RomLoader
from validation.validator import Validator
from fingerprint.fingerprint import FingerprintEngine
from delta.delta_engine import DeltaEngine

from classification.classifier import RegionClassifier
from classification.report import ClassificationReport

from axis.detector import AxisDetector


class Pipeline:
    """
    BLAKKBOX DENSO Studio Main Pipeline

        Load ROMs
            │
        Validation
            │
        Fingerprint
            │
        Delta Analysis
            │
        Region Classification
            │
        Axis Detection
            │
        Map Detection
            │
        Engineering Validation
            │
        Delta Filtering
            │
        Export Report
    """

    def __init__(self):

        # ----------------------------------------------------------
        # Core Modules
        # ----------------------------------------------------------

        self.loader = RomLoader()
        self.validator = Validator()
        self.fingerprint = FingerprintEngine()

        # ----------------------------------------------------------
        # Delta Engine
        # ----------------------------------------------------------

        self.delta = DeltaEngine()

        # ----------------------------------------------------------
        # Region Classification
        # ----------------------------------------------------------

        self.classifier = RegionClassifier()
        self.classification_report = ClassificationReport()

        # ----------------------------------------------------------
        # Axis Detection
        # ----------------------------------------------------------

        self.axis = AxisDetector()

    def execute(self, original_file: str, mod_file: str):

        print("\nLoading ROM files...\n")

        # ==========================================================
        # LOAD ROMS
        # ==========================================================

        original, mod = self.loader.load(
            original_file,
            mod_file
        )

        # ==========================================================
        # VALIDATION
        # ==========================================================

        self.validator.validate(
            original,
            mod
        )

        # ==========================================================
        # ROM FINGERPRINT
        # ==========================================================

        self.fingerprint.analyze(
            original
        )

        # ==========================================================
        # DELTA ANALYSIS
        # ==========================================================

        regions = self.delta.analyze(
            original,
            mod
        )

        # ==========================================================
        # REGION CLASSIFICATION
        # ==========================================================

        regions = self.classifier.classify(
            regions
        )

        self.classification_report.print(
            regions
        )

        # ==========================================================
        # AXIS DETECTION
        # ==========================================================

        axis_candidates = self.axis.analyze(
            regions
        )

        # ==========================================================
        # FUTURE PIPELINE STAGES
        # ==========================================================

        stages = [
            "Map Detection",
            "Engineering Validation",
            "Delta Filtering",
            "Export Report"
        ]

        print()

        for index, stage in enumerate(stages, start=1):
            print(f"[{index}/{len(stages)}] {stage}")

        # ==========================================================
        # SUMMARY
        # ==========================================================

        calibration = sum(
            1 for r in regions
            if getattr(r, "calibration", False)
        )

        valid_axis = sum(
            1 for c in axis_candidates
            if c["valid"]
        )

        print()
        print("=" * 60)
        print("PIPELINE SUMMARY")
        print("=" * 60)

        print(f"Original Size            : {len(original):,} bytes")
        print(f"Modified Size            : {len(mod):,} bytes")
        print(f"Modified Regions         : {len(regions)}")
        print(f"Calibration Candidates   : {calibration}")
        print(f"Valid Axis Candidates    : {valid_axis}")

        print("=" * 60)
        print("Pipeline Complete")
        print("=" * 60)