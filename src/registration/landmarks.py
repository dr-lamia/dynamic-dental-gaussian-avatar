"""Dental landmark helpers for the first maxillary registration experiment."""
from __future__ import annotations
import numpy as np


def maxillary_anchor_template() -> dict[str, np.ndarray]:
    """Synthetic anchor points in mm for a schematic upper arch.

    These are placeholders for engineering tests. Real patient registration
    will use case-specific landmark coordinates.
    """
    return {
        "incisal_midline": np.array([0.0, 22.0, 0.0]),
        "left_canine": np.array([15.0, 14.0, 0.0]),
        "right_canine": np.array([-15.0, 14.0, 0.0]),
        "left_first_molar": np.array([30.0, -2.0, 0.0]),
        "right_first_molar": np.array([-30.0, -2.0, 0.0]),
    }


def paired_arrays(source: dict[str, np.ndarray], target: dict[str, np.ndarray], names: list[str]):
    missing = [n for n in names if n not in source or n not in target]
    if missing:
        raise KeyError(f"Missing landmarks: {missing}")
    return np.vstack([source[n] for n in names]), np.vstack([target[n] for n in names])
