"""Case manifest for a patient-specific dynamic smile-design experiment."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json


@dataclass
class CaseManifest:
    case_id: str
    video: str
    upper_mesh: str
    lower_mesh: str
    design_meshes: list[str]
    bite_mesh: str | None = None
    jaw_motion_csv: str | None = None
    notes: str | None = None

    def validate_extensions(self) -> None:
        video_suffix = Path(self.video).suffix.lower()
        if video_suffix not in {".mp4", ".mov", ".mkv"}:
            raise ValueError(f"Unsupported video: {video_suffix}")

        meshes = [self.upper_mesh, self.lower_mesh, *self.design_meshes]
        if self.bite_mesh:
            meshes.append(self.bite_mesh)
        for mesh in meshes:
            if Path(mesh).suffix.lower() not in {".stl", ".ply", ".obj"}:
                raise ValueError(f"Unsupported mesh: {mesh}")

        if self.jaw_motion_csv and Path(self.jaw_motion_csv).suffix.lower() != ".csv":
            raise ValueError("jaw_motion_csv must be a .csv file")

    def save(self, path: str | Path) -> None:
        self.validate_extensions()
        Path(path).write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
