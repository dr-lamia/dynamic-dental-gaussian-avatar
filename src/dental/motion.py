"""Attach upper and lower dentition to a tracked facial sequence."""
from __future__ import annotations
import numpy as np
from src.registration.rigid import apply_transform
from src.rendering.frame_state import FrameState


def upper_vertices_for_frame(
    vertices_upper: np.ndarray,
    upper_to_face: np.ndarray,
    frame: FrameState,
) -> np.ndarray:
    face_space = apply_transform(vertices_upper, upper_to_face)
    return apply_transform(face_space, frame.face_to_world)


def lower_vertices_for_frame(
    vertices_lower: np.ndarray,
    lower_to_mandible: np.ndarray,
    frame: FrameState,
) -> np.ndarray:
    mandibular = apply_transform(vertices_lower, lower_to_mandible)
    face_space = apply_transform(mandibular, frame.mandible_to_face)
    return apply_transform(face_space, frame.face_to_world)
