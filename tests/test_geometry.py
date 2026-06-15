"""
tests/test_geometry.py
"""

from geometry.rectangle import RectangleDetector


def test_rectangle():

    detector = RectangleDetector()

    rows, cols = detector.detect(256)

    assert rows > 0
    assert cols > 0
