"""Standard jaw-motion representation and CSV I/O for a 4D dental patient.

Tracker-specific files should be converted to this neutral representation before
being fused with facial/head motion. Translations are millimetres and rotations
describe the mandible in the face/maxillary coordinate system.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math
import numpy as np

from src.rendering.frame_state import FrameState


_MATRIX_COLUMNS = [f"m{r}{c}" for r in range(4) for c in range(4)]
_QUAT_COLUMNS = ["tx_mm", "ty_mm", "tz_mm", "qw", "qx", "qy", "qz"]
_EULER_COLUMNS = ["tx_mm", "ty_mm", "tz_mm", "rx_deg", "ry_deg", "rz_deg"]


@dataclass(frozen=True)
class JawMotionSample:
    frame_index: int
    mandible_to_face: np.ndarray
    timestamp_s: float | None = None
    jaw_opening_mm: float | None = None

    def validate(self) -> None:
        if self.frame_index < 0:
            raise ValueError("frame_index must be >= 0")
        if self.mandible_to_face.shape != (4, 4):
            raise ValueError("mandible_to_face must be 4x4")
        if not np.all(np.isfinite(self.mandible_to_face)):
            raise ValueError("mandible_to_face contains non-finite values")
        if not np.allclose(self.mandible_to_face[3], [0.0, 0.0, 0.0, 1.0]):
            raise ValueError("mandible_to_face must be a homogeneous rigid transform")


@dataclass
class JawMotionSequence:
    samples: list[JawMotionSample]

    def __post_init__(self) -> None:
        if not self.samples:
            raise ValueError("JawMotionSequence cannot be empty")
        previous = -1
        for sample in self.samples:
            sample.validate()
            if sample.frame_index <= previous:
                raise ValueError("frame_index values must be strictly increasing")
            previous = sample.frame_index

    def by_frame(self, frame_index: int) -> JawMotionSample:
        for sample in self.samples:
            if sample.frame_index == frame_index:
                return sample
        raise KeyError(f"No jaw-motion sample for frame {frame_index}")

    def to_frame_state(
        self,
        frame_index: int,
        face_to_world: np.ndarray | None = None,
    ) -> FrameState:
        sample = self.by_frame(frame_index)
        if face_to_world is None:
            face_to_world = np.eye(4, dtype=float)
        state = FrameState(
            frame_index=frame_index,
            face_to_world=np.asarray(face_to_world, dtype=float),
            mandible_to_face=sample.mandible_to_face.copy(),
            jaw_opening=sample.jaw_opening_mm,
        )
        state.validate()
        return state


def _quaternion_rotation(qw: float, qx: float, qy: float, qz: float) -> np.ndarray:
    q = np.asarray([qw, qx, qy, qz], dtype=float)
    norm = float(np.linalg.norm(q))
    if norm == 0.0:
        raise ValueError("Quaternion cannot have zero norm")
    w, x, y, z = q / norm
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=float,
    )


def _euler_xyz_rotation(rx_deg: float, ry_deg: float, rz_deg: float) -> np.ndarray:
    """Fixed-axis XYZ rotations, applied X then Y then Z."""
    rx, ry, rz = map(math.radians, (rx_deg, ry_deg, rz_deg))
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)

    rx_m = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]], dtype=float)
    ry_m = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]], dtype=float)
    rz_m = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]], dtype=float)
    return rz_m @ ry_m @ rx_m


def _transform(rotation: np.ndarray, translation_mm: np.ndarray) -> np.ndarray:
    t = np.eye(4, dtype=float)
    t[:3, :3] = rotation
    t[:3, 3] = np.asarray(translation_mm, dtype=float)
    return t


def _optional_float(row: dict[str, str], key: str) -> float | None:
    value = row.get(key)
    if value is None or value.strip() == "":
        return None
    return float(value)


def load_jaw_motion_csv(path: str | Path) -> JawMotionSequence:
    """Load a standardized jaw-motion CSV.

    Required column:
      frame_index

    Pose may be encoded in one of three ways:
      1) m00..m33: full 4x4 homogeneous transform
      2) tx_mm,ty_mm,tz_mm,qw,qx,qy,qz
      3) tx_mm,ty_mm,tz_mm,rx_deg,ry_deg,rz_deg

    Optional columns:
      timestamp_s, jaw_opening_mm
    """
    path = Path(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        if "frame_index" not in fieldnames:
            raise ValueError("Jaw-motion CSV must contain frame_index")

        has_matrix = set(_MATRIX_COLUMNS).issubset(fieldnames)
        has_quat = set(_QUAT_COLUMNS).issubset(fieldnames)
        has_euler = set(_EULER_COLUMNS).issubset(fieldnames)
        if not (has_matrix or has_quat or has_euler):
            raise ValueError(
                "Pose columns not recognized. Supply m00..m33, quaternion pose, "
                "or Euler XYZ pose columns."
            )

        samples: list[JawMotionSample] = []
        for row in reader:
            frame_index = int(row["frame_index"])

            if has_matrix:
                matrix = np.array(
                    [[float(row[f"m{r}{c}"]) for c in range(4)] for r in range(4)],
                    dtype=float,
                )
            elif has_quat:
                rotation = _quaternion_rotation(
                    float(row["qw"]),
                    float(row["qx"]),
                    float(row["qy"]),
                    float(row["qz"]),
                )
                matrix = _transform(
                    rotation,
                    np.array(
                        [float(row["tx_mm"]), float(row["ty_mm"]), float(row["tz_mm"])],
                        dtype=float,
                    ),
                )
            else:
                rotation = _euler_xyz_rotation(
                    float(row["rx_deg"]),
                    float(row["ry_deg"]),
                    float(row["rz_deg"]),
                )
                matrix = _transform(
                    rotation,
                    np.array(
                        [float(row["tx_mm"]), float(row["ty_mm"]), float(row["tz_mm"])],
                        dtype=float,
                    ),
                )

            samples.append(
                JawMotionSample(
                    frame_index=frame_index,
                    timestamp_s=_optional_float(row, "timestamp_s"),
                    jaw_opening_mm=_optional_float(row, "jaw_opening_mm"),
                    mandible_to_face=matrix,
                )
            )

    return JawMotionSequence(samples)


def save_jaw_motion_csv(sequence: JawMotionSequence, path: str | Path) -> None:
    """Save a sequence using the unambiguous full 4x4 transform representation."""
    path = Path(path)
    fields = ["frame_index", "timestamp_s", "jaw_opening_mm", *_MATRIX_COLUMNS]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for sample in sequence.samples:
            row: dict[str, int | float | str] = {
                "frame_index": sample.frame_index,
                "timestamp_s": "" if sample.timestamp_s is None else sample.timestamp_s,
                "jaw_opening_mm": "" if sample.jaw_opening_mm is None else sample.jaw_opening_mm,
            }
            for r in range(4):
                for c in range(4):
                    row[f"m{r}{c}"] = float(sample.mandible_to_face[r, c])
            writer.writerow(row)
