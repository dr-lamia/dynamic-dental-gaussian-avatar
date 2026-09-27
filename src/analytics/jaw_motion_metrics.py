"""Quantitative summaries for standardized mandibular motion."""
from __future__ import annotations
import math
import numpy as np

from src.dental.jaw_motion import JawMotionSequence


def translation_trajectory_mm(sequence: JawMotionSequence) -> np.ndarray:
    return np.vstack([s.mandible_to_face[:3, 3] for s in sequence.samples]).astype(float)


def path_length_mm(sequence: JawMotionSequence) -> float:
    xyz = translation_trajectory_mm(sequence)
    if len(xyz) < 2:
        return 0.0
    return float(np.linalg.norm(np.diff(xyz, axis=0), axis=1).sum())


def displacement_from_start_mm(sequence: JawMotionSequence) -> np.ndarray:
    xyz = translation_trajectory_mm(sequence)
    return np.linalg.norm(xyz - xyz[0], axis=1)


def _relative_rotation_angle_deg(r0: np.ndarray, r1: np.ndarray) -> float:
    relative = r0.T @ r1
    value = (np.trace(relative) - 1.0) / 2.0
    value = float(np.clip(value, -1.0, 1.0))
    return math.degrees(math.acos(value))


def rotation_from_start_deg(sequence: JawMotionSequence) -> np.ndarray:
    r0 = sequence.samples[0].mandible_to_face[:3, :3]
    return np.asarray(
        [_relative_rotation_angle_deg(r0, s.mandible_to_face[:3, :3]) for s in sequence.samples],
        dtype=float,
    )


def summarize_jaw_motion(sequence: JawMotionSequence) -> dict[str, float | int | None]:
    displacement = displacement_from_start_mm(sequence)
    rotation = rotation_from_start_deg(sequence)
    openings = [
        float(s.jaw_opening_mm)
        for s in sequence.samples
        if s.jaw_opening_mm is not None
    ]
    timestamps = [
        float(s.timestamp_s)
        for s in sequence.samples
        if s.timestamp_s is not None
    ]
    duration = None
    if len(timestamps) == len(sequence.samples) and len(timestamps) >= 2:
        duration = timestamps[-1] - timestamps[0]

    return {
        "frames": len(sequence.samples),
        "duration_s": None if duration is None else float(duration),
        "path_length_mm": path_length_mm(sequence),
        "max_displacement_from_start_mm": float(displacement.max()),
        "max_rotation_from_start_deg": float(rotation.max()),
        "max_jaw_opening_mm": None if not openings else float(max(openings)),
    }
