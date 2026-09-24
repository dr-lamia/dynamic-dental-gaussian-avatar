"""Design swapping for motion-controlled dental visualization."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np

from src.registration.rigid import apply_transform


@dataclass(frozen=True)
class MeshState:
    name: str
    vertices: np.ndarray
    faces: np.ndarray


def transform_design_to_world(
    vertices: np.ndarray,
    design_to_upper: np.ndarray,
    upper_to_face: np.ndarray,
    face_to_world: np.ndarray,
) -> np.ndarray:
    """Apply the maxillary transform chain to a design mesh."""
    v = apply_transform(vertices, design_to_upper)
    v = apply_transform(v, upper_to_face)
    v = apply_transform(v, face_to_world)
    return v


def save_obj(path: str | Path, vertices: np.ndarray, faces: np.ndarray) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for v in vertices:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        for tri in faces:
            a, b, c = np.asarray(tri, int) + 1
            f.write(f"f {a} {b} {c}\n")
    return path
