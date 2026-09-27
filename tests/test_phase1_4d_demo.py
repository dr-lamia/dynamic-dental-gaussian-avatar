import numpy as np

from src.analytics.jaw_motion_metrics import (
    displacement_from_start_mm,
    path_length_mm,
    rotation_from_start_deg,
    summarize_jaw_motion,
)
from src.dental.jaw_motion import JawMotionSample, JawMotionSequence
from src.dental.synthetic_arch import (
    build_mandibular_arch,
    default_mandibular_specs,
)


def _transform(tx=0.0, ty=0.0, tz=0.0, rz_deg=0.0):
    a = np.radians(rz_deg)
    c, s = np.cos(a), np.sin(a)
    T = np.eye(4)
    T[:3, :3] = [[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]]
    T[:3, 3] = [tx, ty, tz]
    return T


def test_mandibular_synthetic_arch_has_14_teeth():
    specs = default_mandibular_specs()
    assert len(specs) == 14
    assert specs[0].fdi == 47
    assert specs[-1].fdi == 37

    vertices, faces, labels = build_mandibular_arch()
    assert vertices.shape[1] == 3
    assert faces.shape[1] == 3
    assert len(vertices) == len(labels)
    assert len(set(labels.tolist())) == 14


def test_jaw_motion_metrics_known_trajectory():
    seq = JawMotionSequence([
        JawMotionSample(0, _transform(), timestamp_s=0.0, jaw_opening_mm=0.0),
        JawMotionSample(1, _transform(tx=3.0, rz_deg=30.0), timestamp_s=0.5, jaw_opening_mm=4.0),
        JawMotionSample(2, _transform(tx=3.0, ty=4.0, rz_deg=60.0), timestamp_s=1.0, jaw_opening_mm=8.0),
    ])

    assert np.allclose(displacement_from_start_mm(seq), [0.0, 3.0, 5.0])
    assert np.isclose(path_length_mm(seq), 7.0)
    assert np.allclose(rotation_from_start_deg(seq), [0.0, 30.0, 60.0], atol=1e-7)

    summary = summarize_jaw_motion(seq)
    assert summary["frames"] == 3
    assert summary["duration_s"] == 1.0
    assert np.isclose(summary["path_length_mm"], 7.0)
    assert np.isclose(summary["max_displacement_from_start_mm"], 5.0)
    assert np.isclose(summary["max_rotation_from_start_deg"], 60.0)
    assert summary["max_jaw_opening_mm"] == 8.0
