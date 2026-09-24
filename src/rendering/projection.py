"""Minimal pinhole projection for testing dental-overlay geometry."""
from __future__ import annotations
import numpy as np


def project_points(points_world: np.ndarray, world_to_camera: np.ndarray, K: np.ndarray) -> np.ndarray:
    points_world = np.asarray(points_world, dtype=float)
    if points_world.ndim != 2 or points_world.shape[1] != 3:
        raise ValueError("points_world must be Nx3")
    h = np.c_[points_world, np.ones(len(points_world))]
    cam = (world_to_camera @ h.T).T[:, :3]
    z = cam[:, 2]
    if np.any(z <= 0):
        raise ValueError("All projected points must be in front of the camera")
    uvw = (K @ cam.T).T
    return uvw[:, :2] / uvw[:, 2:3]
