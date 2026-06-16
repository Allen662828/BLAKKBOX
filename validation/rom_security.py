"""Input-file safety checks for local job execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROM_EXTENSIONS = {
    ".bin", ".ori", ".mod", ".hex", ".s19", ".srec", ".mot", ".frf", ".sgm", ".dump"
}


@dataclass(slots=True)
class RomInputSummary:
    original_path: str
    modified_path: str
    original_size: int
    modified_size: int
    same_file: bool
    extension_warning: bool

    def as_dict(self) -> dict[str, str | int | bool]:
        return {
            "original_path": self.original_path,
            "modified_path": self.modified_path,
            "original_size": self.original_size,
            "modified_size": self.modified_size,
            "same_file": self.same_file,
            "extension_warning": self.extension_warning,
        }


class RomSecurityValidator:
    """Fast preflight guard before analysis starts."""

    def validate(self, original_file: str | Path, modified_file: str | Path) -> RomInputSummary:
        original = Path(original_file)
        modified = Path(modified_file)

        if not original.exists():
            raise FileNotFoundError(f"ORIGINAL file not found: {original}")
        if not modified.exists():
            raise FileNotFoundError(f"MOD file not found: {modified}")
        if not original.is_file() or not modified.is_file():
            raise ValueError("ORIGINAL and MOD must both be files")

        same_file = original.resolve() == modified.resolve()
        if same_file:
            raise ValueError("ORIGINAL and MOD point to the same file")

        original_size = original.stat().st_size
        modified_size = modified.stat().st_size
        if original_size <= 0 or modified_size <= 0:
            raise ValueError("ORIGINAL and MOD files must not be empty")

        extension_warning = original.suffix.lower() not in ROM_EXTENSIONS or modified.suffix.lower() not in ROM_EXTENSIONS

        return RomInputSummary(
            original_path=str(original),
            modified_path=str(modified),
            original_size=original_size,
            modified_size=modified_size,
            same_file=same_file,
            extension_warning=extension_warning,
        )
