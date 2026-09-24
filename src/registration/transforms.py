"""Coordinate transform helpers for face, upper arch, mandible and designs."""
from dataclasses import dataclass
import numpy as np


@dataclass
class DentalTransforms:
    face_to_world: np.ndarray
    upper_to_face: np.ndarray
    lower_to_mandible: np.ndarray
    design_to_upper: np.ndarray

    @staticmethod
    def identity() -> "DentalTransforms":
        I = np.eye(4, dtype=float)
        return DentalTransforms(I.copy(), I.copy(), I.copy(), I.copy())
