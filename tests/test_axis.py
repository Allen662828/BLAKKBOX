"""
tests/test_axis.py
"""

from axis.monotonic import MonotonicAnalyzer


def test_monotonic():

    values = [0, 10, 20, 30, 40]

    assert MonotonicAnalyzer().analyze(values)


def test_not_monotonic():

    values = [0, 20, 15, 40]

    assert not MonotonicAnalyzer().analyze(values)
