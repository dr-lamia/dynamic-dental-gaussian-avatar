"""Temporal stability metrics for dental meshes attached to tracked facial motion."""
from __future__ import annotations
import numpy as np


def centroid(points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must be Nx3")
    return points.mean(axis=0)


def framewise_centroid_drift_mm(reference_vertices: np.ndarray, frame_vertices: list[np.ndarray]) -> np.ndarray:
    """Centroid displacement from a reference dental mesh for each frame."""
    c0 = centroid(reference_vertices)
    drifts = []
    for v in frame_vertices:
        drifts.append(float(np.linalg.norm(centroid(v) - c0)))
    return np.asarray(drifts, dtype=float)


def relative_landmark_drift_mm(
    dental_landmarks_per_frame: np.ndarray,
    facial_landmarks_per_frame: np.ndarray,
) -> np.ndarray:
    """Measure change in dental-to-face landmark vectors across frames.

    Arrays are shaped F x K x 3 and must contain corresponding dental/facial
    anchors. This removes whole-head motion and reveals attachment drift.
    """
    d = np.asarray(dental_landmarks_per_frame, float)
    f = np.asarray(facial_landmarks_per_frame, float)
    if d.shape != f.shape or d.ndim != 3 or d.shape[2] != 3:
        raise ValueError("inputs must be matching F x K x 3 arrays")

    rel = d - f
    ref = rel[0]
    err = np.linalg.norm(rel - ref[None, ...], axis=2)
    return err


def summarize_temporal_drift_mm(drift: np.ndarray) -> dict[str, float]:
    drift = np.asarray(drift, float)
    return {
        "mean_mm": float(drift.mean()),
        "max_mm": float(drift.max()),
        "p95_mm": float(np.percentile(drift, 95)),
    }
