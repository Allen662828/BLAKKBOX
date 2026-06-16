from __future__ import annotations

from dataclasses import dataclass

from studio.calibration.map import CalibrationMap
from studio.detection.signature_database import (
    MapSignature,
    SignatureDatabase,
)


@dataclass(slots=True)
class ClassificationResult:
    signature: MapSignature | None
    confidence: float


class MapClassifier:
    """
    First-stage map classifier.

    Current scoring:
        + Geometry
        + Element size

    Future scoring:
        + Axis monotonicity
        + Axis scaling
        + Value distribution
        + Address clustering
        + Region overlap
        + OEM signatures
    """

    @staticmethod
    def classify(
        calibration_map: CalibrationMap,
    ) -> ClassificationResult:

        best_signature = None
        best_score = 0.0

        for signature in SignatureDatabase.all():

            score = 0.0

            if calibration_map.rows == signature.rows:
                score += 0.35

            if calibration_map.columns == signature.columns:
                score += 0.35

            if (
                calibration_map.element_size
                == signature.element_size
            ):
                score += 0.30

            if score > best_score:
                best_score = score
                best_signature = signature

        if best_signature is not None:

            calibration_map.name = best_signature.name
            calibration_map.category = best_signature.category
            calibration_map.description = (
                best_signature.description
            )
            calibration_map.confidence = best_score

        return ClassificationResult(
            signature=best_signature,
            confidence=best_score,
        )

    @staticmethod
    def classify_all(
        maps: list[CalibrationMap],
    ) -> list[ClassificationResult]:

        return [
            MapClassifier.classify(m)
            for m in maps
        ]
