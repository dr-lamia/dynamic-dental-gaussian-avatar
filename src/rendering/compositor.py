"""Image compositing for hybrid facial-avatar + dental rendering."""
from __future__ import annotations
import numpy as np
from src.rendering.occlusion import compose_dental_visibility


def composite_dental_over_face(
    face_rgb: np.ndarray,
    dental_rgb: np.ndarray,
    dental_depth: np.ndarray,
    face_depth: np.ndarray,
    mouth_mask: np.ndarray,
) -> np.ndarray:
    face_rgb = np.asarray(face_rgb)
    dental_rgb = np.asarray(dental_rgb)

    if face_rgb.shape != dental_rgb.shape:
        raise ValueError("face_rgb and dental_rgb must have the same shape")
    if face_rgb.ndim != 3 or face_rgb.shape[2] not in (3, 4):
        raise ValueError("RGB/RGBA image expected")

    visible = compose_dental_visibility(
        dental_depth=dental_depth,
        face_depth=face_depth,
        mouth_mask=mouth_mask,
    )

    out = np.array(face_rgb, copy=True)
    out[visible] = dental_rgb[visible]
    return out
