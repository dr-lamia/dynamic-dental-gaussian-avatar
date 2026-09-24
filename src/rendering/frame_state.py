"""Per-frame face/dental pose container."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass
class FrameState:
    frame_index: int
    face_to_world: np.ndarray
    mandible_to_face: np.ndarray
    jaw_opening: float | None = None

    def validate(self) -> None:
        if self.face_to_world.shape != (4, 4):
            raise ValueError("face_to_world must be 4x4")
        if self.mandible_to_face.shape != (4, 4):
            raise ValueError("mandible_to_face must be 4x4")
