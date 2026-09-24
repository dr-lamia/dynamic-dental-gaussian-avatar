"""Metrics for the first dental-avatar registration benchmark."""
from __future__ import annotations
import numpy as np


def landmark_errors_mm(predicted: np.ndarray, reference: np.ndarray) -> np.ndarray:
    predicted = np.asarray(predicted, float)
    reference = np.asarray(reference, float)
    if predicted.shape != reference.shape:
        raise ValueError("predicted/reference shapes must match")
    return np.linalg.norm(predicted - reference, axis=1)


def summarize_errors_mm(predicted: np.ndarray, reference: np.ndarray) -> dict[str, float]:
    e = landmark_errors_mm(predicted, reference)
    return {
        "mean_mm": float(e.mean()),
        "rmse_mm": float(np.sqrt(np.mean(e ** 2))),
        "max_mm": float(e.max()),
    }
