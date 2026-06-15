"""
classification/classifier.py

Generic region classification.

Regions are classified using simple structural heuristics based
on region length. No assumptions are made about the semantic
meaning of the underlying data.
"""

from configs.config import (
    CLASSIFICATION_MIN_LENGTH,
    UNKNOWN_MIN_LENGTH,
    CALIBRATION_CONFIDENCE,
    UNKNOWN_CONFIDENCE,
    SMALL_EDIT_CONFIDENCE,
)


class RegionClassifier:

    def classify(self, regions):

        for region in regions:

            # ------------------------------------------------------
            # Reset defaults
            # ------------------------------------------------------

            region.calibration = False
            region.region_type = "UNCLASSIFIED"
            region.confidence = 0.0

            length = region.length

            # ------------------------------------------------------
            # Large region
            # ------------------------------------------------------

            if length >= CLASSIFICATION_MIN_LENGTH:

                region.region_type = "CALIBRATION"
                region.calibration = True
                region.confidence = CALIBRATION_CONFIDENCE

            # ------------------------------------------------------
            # Medium region
            # ------------------------------------------------------

            elif length >= UNKNOWN_MIN_LENGTH:

                region.region_type = "UNKNOWN"
                region.confidence = UNKNOWN_CONFIDENCE

            # ------------------------------------------------------
            # Small region
            # ------------------------------------------------------

            else:

                region.region_type = "SMALL_EDIT"
                region.confidence = SMALL_EDIT_CONFIDENCE

        return regions
