from __future__ import annotations

from dataclasses import dataclass

from studio.core.byte_compare import ByteDifference


@dataclass(slots=True)
class FilteredDifference:
    offset: int
    original: int
    modified: int
    filtered: int
    delta: int


class DeltaLogic:
    """
    BLAKKBOX Delta Logic

    FINAL = ORIGINAL + FILTERED_DELTA

    Δ0–5  -> Keep
    Δ5–8  -> ×0.80
    Δ>8   -> ×0.55
    """

    KEEP_LIMIT = 5
    MEDIUM_LIMIT = 8

    MEDIUM_SCALE = 0.80
    LARGE_SCALE = 0.55

    @staticmethod
    def filter_difference(
        difference: ByteDifference,
    ) -> FilteredDifference:

        original = difference.original
        modified = difference.modified

        delta = modified - original

        sign = 1 if delta >= 0 else -1

        magnitude = abs(delta)

        if magnitude <= DeltaLogic.KEEP_LIMIT:

            filtered = modified

        elif magnitude <= DeltaLogic.MEDIUM_LIMIT:

            new_delta = round(
                magnitude * DeltaLogic.MEDIUM_SCALE
            )

            filtered = original + sign * new_delta

        else:

            new_delta = round(
                magnitude * DeltaLogic.LARGE_SCALE
            )

            filtered = original + sign * new_delta

        filtered = max(
            0,
            min(
                255,
                filtered,
            ),
        )

        return FilteredDifference(
            offset=difference.offset,
            original=original,
            modified=modified,
            filtered=filtered,
            delta=filtered - original,
        )

    @staticmethod
    def apply(
        differences: list[ByteDifference],
    ) -> list[FilteredDifference]:

        return [
            DeltaLogic.filter_difference(d)
            for d in differences
        ]

    @staticmethod
    def build_final_bin(
        original: bytes,
        filtered: list[FilteredDifference],
    ) -> bytes:

        result = bytearray(original)

        for diff in filtered:

            result[diff.offset] = diff.filtered

        return bytes(result)
