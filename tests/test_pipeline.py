"""
tests/test_pipeline.py
"""

from core.pipeline import Pipeline


def test_pipeline_creation():

    pipeline = Pipeline()

    assert pipeline is not None

    assert pipeline.loader is not None
    assert pipeline.validator is not None
    assert pipeline.fingerprint is not None
    assert pipeline.delta is not None
    assert pipeline.classifier is not None
    assert pipeline.axis is not None
    assert pipeline.geometry is not None
