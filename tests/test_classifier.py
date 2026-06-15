"""
tests/test_classifier.py
"""

from classification.classifier import RegionClassifier
from delta.region import DeltaRegion


def test_large_region():

    region = DeltaRegion(0, 200)

    RegionClassifier().classify([region])

    assert region.calibration is True
    assert region.region_type == "CALIBRATION"


def test_unknown():

    region = DeltaRegion(0, 25)

    RegionClassifier().classify([region])

    assert region.region_type == "UNKNOWN"


def test_small():

    region = DeltaRegion(0, 5)

    RegionClassifier().classify([region])

    assert region.region_type == "SMALL_EDIT"
