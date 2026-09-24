"""Depth-aware dental occlusion utilities.

The goal is to prevent dental geometry from rendering through lips/cheeks.
This module stays renderer-agnostic: it operates on depth and mouth masks.
"""
from __future__ import annotations
import numpy as np


def compose_dental_visibility(
    dental_depth: np.ndarray,
    face_depth: np.ndarray,
    mouth_mask: np.ndarray,
    eps: float = 1e-4,
) -> np.ndarray:
    """Return a boolean visibility mask for dental pixels.

    A dental pixel is visible only if:
    1) it lies inside the mouth opening mask, and
    2) it is not behind the facial surface at that pixel.

    Depth arrays should use the same camera convention: smaller positive depth
    means closer to the camera.
    """
    dental_depth = np.asarray(dental_depth, dtype=float)
    face_depth = np.asarray(face_depth, dtype=float)
    mouth_mask = np.asarray(mouth_mask, dtype=bool)

    if dental_depth.shape != face_depth.shape or dental_depth.shape != mouth_mask.shape:
        raise ValueError("dental_depth, face_depth, and mouth_mask must have matching shapes")

    valid_dental = np.isfinite(dental_depth) & (dental_depth > 0)
    valid_face = np.isfinite(face_depth) & (face_depth > 0)

    in_mouth = mouth_mask & valid_dental
    in_front_of_face = (~valid_face) | (dental_depth <= face_depth + eps)

    return in_mouth & in_front_of_face


def apply_visibility_mask(image: np.ndarray, visibility: np.ndarray, fill_value=0):
    image = np.asarray(image)
    visibility = np.asarray(visibility, dtype=bool)
    if image.shape[:2] != visibility.shape:
        raise ValueError("visibility must match image height/width")

    out = np.array(image, copy=True)
    if out.ndim == 2:
        out[~visibility] = fill_value
    else:
        out[~visibility, ...] = fill_value
    return out
