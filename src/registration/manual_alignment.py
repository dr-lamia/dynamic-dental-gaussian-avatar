"""Reproducible manual dental alignment parameters.

This module is for the public cross-subject engineering demo. It stores explicit
rotation/translation values so alignment can be replayed exactly. It does not
estimate patient-specific anatomy.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import math
import numpy as np

from src.registration.rigid import apply_transform


@dataclass
class ManualAlignment:
    translation_mm: tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation_deg_xyz: tuple[float, float, float] = (0.0, 0.0, 0.0)

    def matrix(self) -> np.ndarray:
        rx, ry, rz = [math.radians(v) for v in self.rotation_deg_xyz]
        sx, cx = math.sin(rx), math.cos(rx)
        sy, cy = math.sin(ry), math.cos(ry)
        sz, cz = math.sin(rz), math.cos(rz)

        Rx = np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]], float)
        Ry = np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]], float)
        Rz = np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]], float)
        R = Rz @ Ry @ Rx

        T = np.eye(4, dtype=float)
        T[:3,:3] = R
        T[:3,3] = np.asarray(self.translation_mm, float)
        return T

    def apply(self, points: np.ndarray) -> np.ndarray:
        return apply_transform(points, self.matrix())

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            **asdict(self),
            "matrix": self.matrix().tolist(),
            "units": "mm",
            "note": "Manual public-demo alignment only; not anatomical validation."
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: str | Path) -> "ManualAlignment":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            translation_mm=tuple(float(x) for x in data["translation_mm"]),
            rotation_deg_xyz=tuple(float(x) for x in data["rotation_deg_xyz"]),
        )
