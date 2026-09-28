"""Adapter for MultiFace tracked meshes and head-pose transforms."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import numpy as np


_FLOAT_RE = re.compile(
    r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
)


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
    """Load a MultiFace head-pose transform.

    Accepts 4x4 or 3x4 matrices written with whitespace, commas, brackets,
    or scientific notation. A 3x4 matrix is promoted to homogeneous 4x4 form.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    values = [float(x) for x in _FLOAT_RE.findall(text)]

    if len(values) >= 16:
        matrix = np.asarray(values[:16], dtype=float).reshape(4, 4)
    elif len(values) >= 12:
        matrix = np.eye(4, dtype=float)
        matrix[:3, :] = np.asarray(values[:12], dtype=float).reshape(3, 4)
    else:
        preview = text[:300].replace("\n", " | ")
        raise ValueError(
            f"Could not parse transform from {path}; "
            f"found {len(values)} numeric values. Preview: {preview}"
        )

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
