"""Small dependency-light settings loader for BLAKKBOX.

The pipeline works without PyYAML. If PyYAML is installed, YAML config files are
loaded. If it is not installed, safe defaults are used.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class DeltaRuleSettings:
    small_max: int = 5
    medium_max: int = 8
    medium_multiplier: float = 0.80
    large_multiplier: float = 0.55
    preserve_mod_zero: bool = True


@dataclass(slots=True)
class ExportSettings:
    enhanced_name: str = "enhanced.bin"
    json_report_name: str = "analysis.json"
    markdown_report_name: str = "analysis.md"
    manifest_name: str = "manifest.json"
    write_markdown: bool = True
    write_manifest: bool = True


@dataclass(slots=True)
class PipelineSettings:
    delta: DeltaRuleSettings = field(default_factory=DeltaRuleSettings)
    export: ExportSettings = field(default_factory=ExportSettings)


def _load_yaml_if_available(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore[import-not-found]
    except Exception:
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        return {}
    return data


def load_settings(config_file: str | Path | None = None) -> PipelineSettings:
    settings = PipelineSettings()
    if config_file is None:
        default_path = Path("configs/pipeline.yaml")
        data = _load_yaml_if_available(default_path)
    else:
        data = _load_yaml_if_available(Path(config_file))

    delta = data.get("delta", {}) if isinstance(data.get("delta", {}), dict) else {}
    export = data.get("export", {}) if isinstance(data.get("export", {}), dict) else {}

    if delta:
        settings.delta.small_max = int(delta.get("small_max", settings.delta.small_max))
        settings.delta.medium_max = int(delta.get("medium_max", settings.delta.medium_max))
        settings.delta.medium_multiplier = float(delta.get("medium_multiplier", settings.delta.medium_multiplier))
        settings.delta.large_multiplier = float(delta.get("large_multiplier", settings.delta.large_multiplier))
        settings.delta.preserve_mod_zero = bool(delta.get("preserve_mod_zero", settings.delta.preserve_mod_zero))

    if export:
        settings.export.enhanced_name = str(export.get("enhanced_name", settings.export.enhanced_name))
        settings.export.json_report_name = str(export.get("json_report_name", settings.export.json_report_name))
        settings.export.markdown_report_name = str(export.get("markdown_report_name", settings.export.markdown_report_name))
        settings.export.manifest_name = str(export.get("manifest_name", settings.export.manifest_name))
        settings.export.write_markdown = bool(export.get("write_markdown", settings.export.write_markdown))
        settings.export.write_manifest = bool(export.get("write_manifest", settings.export.write_manifest))

    return settings
