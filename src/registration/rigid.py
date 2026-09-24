"""Rigid 3D registration utilities.

The first MVP uses manually identified corresponding landmarks to obtain a
reproducible initialization. ICP or another surface refinement can be added
after this transform.
"""
from __future__ import annotations
import numpy as np


def estimate_rigid_transform(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Estimate a least-squares rigid transform mapping source -> target.

    Parameters
    ----------
    source, target:
        Nx3 arrays of corresponding 3D landmarks in the same metric units.

    Returns
    -------
    4x4 homogeneous transformation matrix.

    Notes
    -----
    This is a Kabsch/SVD rigid fit: rotation + translation only, no scale.
    """
    source = np.asarray(source, dtype=float)
    target = np.asarray(target, dtype=float)
    if source.shape != target.shape or source.ndim != 2 or source.shape[1] != 3:
        raise ValueError("source and target must be matching Nx3 arrays")
    if source.shape[0] < 3:
        raise ValueError("At least 3 corresponding landmarks are required")

    cs = source.mean(axis=0)
    ct = target.mean(axis=0)
    xs = source - cs
    xt = target - ct

    h = xs.T @ xt
    u, _, vt = np.linalg.svd(h)
    r = vt.T @ u.T
    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1
        r = vt.T @ u.T

    t = ct - r @ cs
    T = np.eye(4, dtype=float)
    T[:3, :3] = r
    T[:3, 3] = t
    return T


def apply_transform(points: np.ndarray, transform: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    transform = np.asarray(transform, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must be Nx3")
    if transform.shape != (4, 4):
        raise ValueError("transform must be 4x4")
    h = np.c_[points, np.ones(len(points))]
    return (transform @ h.T).T[:, :3]


def registration_rmse(source: np.ndarray, target: np.ndarray, transform: np.ndarray) -> float:
    moved = apply_transform(source, transform)
    return float(np.sqrt(np.mean(np.sum((moved - target) ** 2, axis=1))))
