"""VHAP/FLAME region bridge for dental occlusion.

VHAP's FLAME implementation exposes named mask regions including
lip_outside_ring_upper and lip_outside_ring_lower. We keep only the names and
the extraction contract here; no VHAP source code or FLAME assets are copied.
"""
from __future__ import annotations
import numpy as np

UPPER_LIP_REGION = "lip_outside_ring_upper"
LOWER_LIP_REGION = "lip_outside_ring_lower"


def mouth_polygon_from_rings(
    upper_xy: np.ndarray,
    lower_xy: np.ndarray,
) -> np.ndarray:
    """Build a closed mouth-opening polygon from ordered upper/lower lip rings.

    upper_xy and lower_xy should each be Nx2 and ordered left-to-right using
    the upstream VHAP/FLAME region order.
    """
    upper_xy = np.asarray(upper_xy, dtype=float)
    lower_xy = np.asarray(lower_xy, dtype=float)
    if upper_xy.ndim != 2 or upper_xy.shape[1] != 2:
        raise ValueError("upper_xy must be Nx2")
    if lower_xy.ndim != 2 or lower_xy.shape[1] != 2:
        raise ValueError("lower_xy must be Nx2")
    if len(upper_xy) < 2 or len(lower_xy) < 2:
        raise ValueError("lip rings must contain at least two points")

    # Upper left→right, lower right→left closes the aperture polygon.
    return np.vstack([upper_xy, lower_xy[::-1]])


def aperture_height_px(upper_xy: np.ndarray, lower_xy: np.ndarray) -> float:
    """Median vertical separation between matched upper/lower ring samples."""
    upper_xy = np.asarray(upper_xy, dtype=float)
    lower_xy = np.asarray(lower_xy, dtype=float)
    n = min(len(upper_xy), len(lower_xy))
    if n == 0:
        raise ValueError("empty lip ring")
    return float(np.median(np.abs(lower_xy[:n, 1] - upper_xy[:n, 1])))
