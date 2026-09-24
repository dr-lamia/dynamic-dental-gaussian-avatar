import numpy as np
from src.analytics.temporal_stability import relative_landmark_drift_mm, summarize_temporal_drift_mm


def test_relative_drift_ignores_whole_head_motion():
    dental = np.array([
        [[0., 0., 0.]],
        [[10., 0., 0.]],
    ])
    face = np.array([
        [[0., 1., 0.]],
        [[10., 1., 0.]],
    ])
    drift = relative_landmark_drift_mm(dental, face)
    assert np.allclose(drift, 0.0)


def test_relative_drift_detects_attachment_error():
    dental = np.array([
        [[0., 0., 0.]],
        [[10., 0., 0.]],
    ])
    face = np.array([
        [[0., 1., 0.]],
        [[10., 3., 0.]],
    ])
    drift = relative_landmark_drift_mm(dental, face)
    assert np.isclose(drift[1, 0], 2.0)
    summary = summarize_temporal_drift_mm(drift)
    assert summary["max_mm"] == 2.0
