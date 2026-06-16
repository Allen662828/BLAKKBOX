"""BLAKKBOX filtered-delta processing.

The filter only operates on offsets that already differ between ORIGINAL and
MOD. It never creates new modified regions and never applies a MOD value of 0
when zero preservation is enabled.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class DeltaFilterRules:
    small_max: int = 5
    medium_max: int = 8
    medium_multiplier: float = 0.80
    large_multiplier: float = 0.55
    preserve_mod_zero: bool = True


def _clamp_byte(value: int) -> int:
    return max(0, min(255, int(value)))


@dataclass(slots=True)
class FilteredDeltaResult:
    values: dict[int, int] = field(default_factory=dict)
    kept_offsets: list[int] = field(default_factory=list)
    reduced_medium_offsets: list[int] = field(default_factory=list)
    reduced_large_offsets: list[int] = field(default_factory=list)
    skipped_zero_offsets: list[int] = field(default_factory=list)

    @property
    def allowed_offsets(self) -> set[int]:
        return set(self.values)

    def summary(self) -> dict[str, int]:
        return {
            "final_changed_offsets": len(self.values),
            "small_deltas_kept": len(self.kept_offsets),
            "medium_deltas_reduced": len(self.reduced_medium_offsets),
            "large_deltas_reduced": len(self.reduced_large_offsets),
            "mod_zero_offsets_skipped": len(self.skipped_zero_offsets),
        }


class DeltaFilter:
    """Apply BLAKKBOX byte-level delta rules.

    Default rules:
    - Δ0–5: keep MOD value
    - Δ5–8: apply 80% of delta
    - Δ>8: apply 55% of delta
    - MOD value == 0: skip, preserve ORIGINAL
    """

    def __init__(self, rules: DeltaFilterRules | None = None) -> None:
        self.rules = rules or DeltaFilterRules()

    def apply(
        self,
        original: bytes,
        modified: bytes,
        regions: list[Any],
    ) -> FilteredDeltaResult:
        if len(original) != len(modified):
            raise ValueError("ORIGINAL and MOD size mismatch")

        result = FilteredDeltaResult()

        for region in regions:
            start = int(getattr(region, "start"))
            end = int(getattr(region, "end"))

            if start < 0 or end >= len(original) or end < start:
                raise ValueError(f"Invalid delta region: {start}-{end}")

            for offset in range(start, end + 1):
                original_value = original[offset]
                mod_value = modified[offset]

                if original_value == mod_value:
                    continue

                if self.rules.preserve_mod_zero and mod_value == 0:
                    result.skipped_zero_offsets.append(offset)
                    continue

                delta = mod_value - original_value
                magnitude = abs(delta)

                if magnitude <= self.rules.small_max:
                    final_value = mod_value
                    result.kept_offsets.append(offset)
                elif magnitude <= self.rules.medium_max:
                    final_value = original_value + round(delta * self.rules.medium_multiplier)
                    result.reduced_medium_offsets.append(offset)
                else:
                    final_value = original_value + round(delta * self.rules.large_multiplier)
                    result.reduced_large_offsets.append(offset)

                final_value = _clamp_byte(final_value)
                if final_value != original_value:
                    result.values[offset] = final_value

        return result
