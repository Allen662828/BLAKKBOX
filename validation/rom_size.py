from validation.result import ValidationResult


class RomSizeValidator:

    def validate(self, original: bytes, mod: bytes):

        if len(original) != len(mod):
            return ValidationResult(
                False,
                "ROM Size",
                f"Size mismatch ({len(original)} != {len(mod)})"
            )

        return ValidationResult(
            True,
            "ROM Size",
            f"ROM size OK ({len(original):,} bytes)"
        )