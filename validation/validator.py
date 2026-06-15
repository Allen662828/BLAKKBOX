"""
validation/validator.py

Main validation pipeline.

Executes all registered validators before the remaining
analysis stages are allowed to run.
"""

from __future__ import annotations

from validation.rom_size import RomSizeValidator

from core.logger import (
    section,
    info,
    error,
)


class Validator:
    """
    Main validation controller.
    """

    def __init__(self) -> None:

        self.validators = [
            RomSizeValidator(),
        ]

    def validate(
        self,
        original: bytes,
        modified: bytes,
    ) -> None:
        """
        Execute every registered validator.

        Raises
        ------
        RuntimeError
            If any validator fails.
        """

        section("VALIDATION")

        passed = 0
        failed = 0

        for validator in self.validators:

            result = validator.validate(
                original,
                modified
            )

            if result.passed:

                passed += 1

                info(
                    f"[PASS] {result.name:<24} "
                    f"{result.message}"
                )

            else:

                failed += 1

                error(
                    f"[FAIL] {result.name:<24} "
                    f"{result.message}"
                )

                raise RuntimeError(result.message)

        info("")
        info(f"Validators Passed : {passed}")
        info(f"Validators Failed : {failed}")
