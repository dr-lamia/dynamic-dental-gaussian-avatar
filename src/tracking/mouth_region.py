"""Mouth-region utilities for tracked facial sequences.

For the first prototype, we represent the mouth opening as a 2D polygon.
Later this can be produced directly from projected FLAME lip landmarks.
"""
from __future__ import annotations
import numpy as np


def polygon_mask(height: int, width: int, polygon_xy: np.ndarray) -> np.ndarray:
    """Rasterize a simple polygon using a ray-casting test."""
    poly = np.asarray(polygon_xy, dtype=float)
    if poly.ndim != 2 or poly.shape[1] != 2 or len(poly) < 3:
        raise ValueError("polygon_xy must be Nx2 with N>=3")

    yy, xx = np.mgrid[:height, :width]
    x = xx.ravel().astype(float)
    y = yy.ravel().astype(float)

    inside = np.zeros_like(x, dtype=bool)
    x0, y0 = poly[-1]
    for x1, y1 in poly:
        cond = ((y1 > y) != (y0 > y))
        xinters = (x0 - x1) * (y - y1) / ((y0 - y1) + 1e-12) + x1
        inside ^= cond & (x < xinters)
        x0, y0 = x1, y1

    return inside.reshape(height, width)


def mouth_polygon_from_landmarks(
    landmarks_xy: np.ndarray,
    outer_lip_indices: list[int],
) -> np.ndarray:
    landmarks_xy = np.asarray(landmarks_xy, dtype=float)
    if landmarks_xy.ndim != 2 or landmarks_xy.shape[1] != 2:
        raise ValueError("landmarks_xy must be Nx2")
    return landmarks_xy[np.asarray(outer_lip_indices, dtype=int)]
