"""Main BLAKKBOX analysis and enhancement pipeline."""

from __future__ import annotations

from pathlib import Path

from axis.detector import AxisDetector
from classification.classifier import RegionClassifier
from classification.report import ClassificationReport
from config.settings import DeltaRuleSettings, load_settings
from core.logger import info, kv, section
from delta.delta_engine import DeltaEngine
from delta.filtered_delta import DeltaFilter, DeltaFilterRules
from delta.final_merge import FinalMerge
from export.manifest import ManifestExporter
from export.markdown_report import MarkdownReportExporter
from export.report_exporter import ReportExporter
from fingerprint.fingerprint import FingerprintEngine
from geometry.detector import GeometryDetector
from loader.rom_loader import RomLoader
from protection.protected_regions import ProtectedRegionGuard
from validation.final_integrity import FinalIntegrityValidator
from validation.rom_security import RomSecurityValidator
from validation.validator import Validator


class Pipeline:
    """Main analysis pipeline.

    Output rule:
        ENHANCED_BIN = ORIGINAL_BIN + FILTERED_DELTA
    """

    def __init__(self) -> None:
        self.loader = RomLoader()
        self.validator = Validator()
        self.input_security = RomSecurityValidator()
        self.fingerprint = FingerprintEngine()
        self.delta = DeltaEngine()
        self.classifier = RegionClassifier()
        self.classification_report = ClassificationReport()
        self.axis = AxisDetector()
        self.geometry = GeometryDetector()
        self.final_merge = FinalMerge()
        self.final_validator = FinalIntegrityValidator()
        self.report_exporter = ReportExporter()
        self.markdown_exporter = MarkdownReportExporter()
        self.manifest_exporter = ManifestExporter()

    @staticmethod
    def _to_filter_rules(settings: DeltaRuleSettings) -> DeltaFilterRules:
        return DeltaFilterRules(
            small_max=settings.small_max,
            medium_max=settings.medium_max,
            medium_multiplier=settings.medium_multiplier,
            large_multiplier=settings.large_multiplier,
            preserve_mod_zero=settings.preserve_mod_zero,
        )

    def execute(
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
        settings = load_settings(config_file)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        input_summary = self.input_security.validate(original_file, modified_file)
        if strict and input_summary.extension_warning:
            raise RuntimeError("Strict mode: one or more input files use an unexpected ROM extension")

        info("Loading files...")
        original, modified = self.loader.load(original_file, modified_file)
        self.validator.validate(original, modified)

        fingerprint = self.fingerprint.analyze(original)

        changed_offsets = set(self.delta.extractor.extract(original, modified))
        regions = self.delta.analyze(original, modified)
        delta_summary = self.delta.statistics.summarize(regions)

        regions = self.classifier.classify(regions)
        classification_summary = self.classification_report.print(regions)

        axis_candidates = self.axis.analyze(original, regions)
        valid_axis = [
            candidate for candidate in axis_candidates if candidate.get("valid", False)
        ]
        axis_summary = {
            "total": len(axis_candidates),
            "valid": len(valid_axis),
            "rejected": len(axis_candidates) - len(valid_axis),
        }

        geometry_candidates = self.geometry.analyze(valid_axis)
        valid_geometry = [
            candidate for candidate in geometry_candidates if candidate.get("valid", False)
        ]
        geometry_summary = {
            "total": len(geometry_candidates),
            "valid": len(valid_geometry),
            "rejected": len(geometry_candidates) - len(valid_geometry),
        }

        section("FILTERED DELTA")
        delta_filter = DeltaFilter(self._to_filter_rules(settings.delta))
        filtered_delta = delta_filter.apply(original, modified, regions)
        filtered_summary = filtered_delta.summary()
        kv("Final Changed Offsets", filtered_summary["final_changed_offsets"])
        kv("Small Deltas Kept", filtered_summary["small_deltas_kept"])
        kv("Medium Deltas Reduced", filtered_summary["medium_deltas_reduced"])
        kv("Large Deltas Reduced", filtered_summary["large_deltas_reduced"])
        kv("MOD Zero Skipped", filtered_summary["mod_zero_offsets_skipped"])

        guard = ProtectedRegionGuard.from_yaml(protected_config or "configs/protected_regions.yaml")
        protected_hits = guard.find_hits(filtered_delta.values)
        if protected_hits:
            guard.validate(filtered_delta.values)

        final_bytes = self.final_merge.merge(original, filtered_delta.values)
        final_validation = self.final_validator.validate(
            original=original,
            modified=modified,
            final=final_bytes,
            existing_delta_offsets=changed_offsets,
            allowed_offsets=filtered_delta.allowed_offsets,
        ).as_dict()

        output_bin: str | None = None
        if dry_run:
            info("Dry run enabled: enhanced BIN was not exported.")
        else:
            bin_path = output_path / settings.export.enhanced_name
            exported = self.final_merge.export(final_bytes, bin_path)
            output_bin = str(exported)

        report_file = self.report_exporter.export(
            output_dir=output_dir,
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
            filtered_delta_summary=filtered_summary,
            final_validation=final_validation,
            protected_hits=[hit.as_dict() for hit in protected_hits],
            input_security=input_summary.as_dict(),
            output_bin=output_bin,
            json_name=settings.export.json_report_name,
        )

        markdown_file: str | None = None
        if write_markdown and settings.export.write_markdown:
            report = self.report_exporter.build_report(
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
                filtered_delta_summary=filtered_summary,
                final_validation=final_validation,
                protected_hits=[hit.as_dict() for hit in protected_hits],
                input_security=input_summary.as_dict(),
                output_bin=output_bin,
            )
            markdown_path = output_path / settings.export.markdown_report_name
            self.markdown_exporter.export(markdown_path, report)
            markdown_file = str(markdown_path)

        manifest_file: str | None = None
        if write_manifest and settings.export.write_manifest:
            manifest = self.manifest_exporter.build(
                original_file=original_file,
                modified_file=modified_file,
                output_bin=output_bin,
                report_file=report_file,
                status="PASS",
                extra={
                    "dry_run": dry_run,
                    "strict": strict,
                    "final_validation": final_validation,
                    "filtered_delta": filtered_summary,
                },
            )
            manifest_path = output_path / settings.export.manifest_name
            self.manifest_exporter.export(manifest_path, manifest)
            manifest_file = str(manifest_path)

        section("PIPELINE SUMMARY")
        kv("Original Size", f"{len(original):,} bytes")
        kv("Modified Size", f"{len(modified):,} bytes")
        kv("Modified Regions", len(regions))
        kv("Calibration Regions", classification_summary["calibration"])
        kv("Axis Candidates", axis_summary["total"])
        kv("Valid Axis", axis_summary["valid"])
        kv("Geometry Candidates", geometry_summary["total"])
        kv("Valid Geometry", geometry_summary["valid"])
        kv("Final Formula", "ENHANCED_BIN = ORIGINAL_BIN + FILTERED_DELTA")
        info("Analysis Complete")

        return {
            "fingerprint": fingerprint,
            "delta": delta_summary,
            "filtered_delta": filtered_summary,
            "classification": classification_summary,
            "axis": axis_summary,
            "geometry": geometry_summary,
            "final_validation": final_validation,
            "protected_region_hits": [hit.as_dict() for hit in protected_hits],
            "output_bin": output_bin,
            "report_file": str(report_file),
            "markdown_file": markdown_file,
            "manifest_file": manifest_file,
            "strict": strict,
        }
