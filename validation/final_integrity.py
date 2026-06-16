"""Final BLAKKBOX integrity gate."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FinalIntegritySummary:
    file_size_preserved: bool
    no_new_modified_regions: bool
    untouched_bytes_preserved: bool
    mod_zero_values_not_applied: bool
    final_changed_bytes: int

    def as_dict(self) -> dict[str, bool | int]:
        return {
            "file_size_preserved": self.file_size_preserved,
            "no_new_modified_regions": self.no_new_modified_regions,
            "untouched_bytes_preserved": self.untouched_bytes_preserved,
            "mod_zero_values_not_applied": self.mod_zero_values_not_applied,
            "final_changed_bytes": self.final_changed_bytes,
        }


class FinalIntegrityValidator:
    """Validate that FINAL is only ORIGINAL + allowed FILTERED_DELTA."""

    def validate(
        self,
        original: bytes,
        modified: bytes,
        final: bytes,
        existing_delta_offsets: set[int],
        allowed_offsets: set[int],
    ) -> FinalIntegritySummary:
        if len(original) != len(modified):
            raise RuntimeError("ORIGINAL and MOD size mismatch")

        file_size_preserved = len(original) == len(final)
        if not file_size_preserved:
            raise RuntimeError("FINAL size does not match ORIGINAL size")

        final_delta_offsets = {
            offset
            for offset, (original_value, final_value) in enumerate(zip(original, final))
            if original_value != final_value
        }

        new_offsets = final_delta_offsets - existing_delta_offsets
        if new_offsets:
            raise RuntimeError(
                "FINAL created new modified offsets outside original MOD delta: "
                f"{sorted(new_offsets)[:10]}"
            )

        outside_allowed = final_delta_offsets - allowed_offsets
        if outside_allowed:
            raise RuntimeError(
                "FINAL changed bytes outside filtered-delta allowlist: "
                f"{sorted(outside_allowed)[:10]}"
            )

        zero_applied = {
            offset
            for offset in final_delta_offsets
            if modified[offset] == 0
        }
        if zero_applied:
            raise RuntimeError(
                "FINAL applied MOD zero-values, which is blocked: "
                f"{sorted(zero_applied)[:10]}"
            )

        # Strong OEM preservation check: every byte not explicitly allowed must
        # remain byte-for-byte identical to ORIGINAL.
        corrupted_offsets = [
            offset
            for offset, (original_value, final_value) in enumerate(zip(original, final))
            if offset not in allowed_offsets and original_value != final_value
        ]
        if corrupted_offsets:
            raise RuntimeError(
                "FINAL corrupted untouched OEM bytes: "
                f"{corrupted_offsets[:10]}"
            )

        return FinalIntegritySummary(
            file_size_preserved=True,
            no_new_modified_regions=True,
            untouched_bytes_preserved=True,
            mod_zero_values_not_applied=True,
            final_changed_bytes=len(final_delta_offsets),
        )
