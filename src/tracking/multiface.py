"""Adapter for MultiFace tracked meshes and head-pose transforms."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np


@dataclass(frozen=True)
class MultiFaceFrame:
    frame_id: str
    mesh_path: Path
    transform_path: Path


@dataclass
class MultiFaceSequence:
    expression: str
    frames: list[MultiFaceFrame]

    def validate(self) -> None:
        if not self.frames:
            raise ValueError(f"No frames found for expression {self.expression}")
        ids = [f.frame_id for f in self.frames]
        if ids != sorted(ids):
            raise ValueError("Frames are not sorted")
        for frame in self.frames:
            if not frame.mesh_path.is_file():
                raise FileNotFoundError(frame.mesh_path)
            if not frame.transform_path.is_file():
                raise FileNotFoundError(frame.transform_path)


def load_headpose_matrix(path: str | Path) -> np.ndarray:
    """Load a MultiFace *_transform.txt 4x4 matrix.

    The official MultiFace data structure documents one head-pose transform file
    alongside each tracked OBJ frame. This loader accepts whitespace-separated
    matrices with optional extra blank lines.
    """
    path = Path(path)
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        try:
            row = [float(x) for x in parts]
        except ValueError:
            continue
        if len(row) == 4:
            rows.append(row)

    if len(rows) < 4:
        raise ValueError(f"Could not parse a 4x4 transform from {path}")

    matrix = np.asarray(rows[:4], dtype=float)
    if matrix.shape != (4, 4):
        raise ValueError(f"Expected 4x4 transform in {path}")
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"Non-finite values in {path}")
    return matrix


def discover_expression(
    multiface_root: str | Path,
    expression: str,
) -> MultiFaceSequence:
    """Discover OBJ/head-pose frame pairs for one MultiFace expression."""
    root = Path(multiface_root)
    tracked = root / "tracked_mesh" / expression
    if not tracked.is_dir():
        raise FileNotFoundError(
            f"Expression folder not found: {tracked}"
        )

    frames: list[MultiFaceFrame] = []
    for mesh_path in sorted(tracked.glob("*.obj")):
        frame_id = mesh_path.stem
        transform_path = tracked / f"{frame_id}_transform.txt"
        if transform_path.exists():
            frames.append(
                MultiFaceFrame(
                    frame_id=frame_id,
                    mesh_path=mesh_path,
                    transform_path=transform_path,
                )
            )

    sequence = MultiFaceSequence(expression=expression, frames=frames)
    sequence.validate()
    return sequence


def discover_dental_subset(multiface_root: str | Path) -> dict[str, MultiFaceSequence]:
    expressions = [
        "E001_Neutral_Eyes_Open",
        "E009_Smile_Mouth_Open",
        "E029_Show_All_Teeth",
    ]
    return {
        expression: discover_expression(multiface_root, expression)
        for expression in expressions
    }
