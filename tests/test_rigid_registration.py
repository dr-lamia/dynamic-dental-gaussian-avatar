import numpy as np
from src.registration.rigid import estimate_rigid_transform, apply_transform, registration_rmse


def test_rigid_transform_recovers_known_translation():
    source = np.array([
        [0.0, 0.0, 0.0],
        [10.0, 0.0, 0.0],
        [0.0, 10.0, 0.0],
        [0.0, 0.0, 10.0],
    ])
    shift = np.array([5.0, -3.0, 2.0])
    target = source + shift
    T = estimate_rigid_transform(source, target)
    moved = apply_transform(source, T)
    assert np.allclose(moved, target, atol=1e-8)
    assert registration_rmse(source, target, T) < 1e-8


def test_rigid_transform_does_not_introduce_scale():
    source = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ])
    target = source * 2.0
    T = estimate_rigid_transform(source, target)
    R = T[:3, :3]
    assert np.isclose(np.linalg.det(R), 1.0, atol=1e-8)
