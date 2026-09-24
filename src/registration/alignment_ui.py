"""Helpers for a simple interactive rigid-alignment UI.

The UI itself can be implemented in Streamlit or another frontend. These
functions define the parameter contract so the saved transform is independent
of the UI technology.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class AlignmentLimits:
    translation_min_mm: float = -100.0
    translation_max_mm: float = 100.0
    rotation_min_deg: float = -45.0
    rotation_max_deg: float = 45.0
    translation_step_mm: float = 0.5
    rotation_step_deg: float = 0.5


DEFAULT_LIMITS = AlignmentLimits()


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))
