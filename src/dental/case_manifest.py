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
    notes: str | None = None

    def validate_extensions(self) -> None:
        video_suffix = Path(self.video).suffix.lower()
        if video_suffix not in {".mp4", ".mov", ".mkv"}:
            raise ValueError(f"Unsupported video: {video_suffix}")
        for mesh in [self.upper_mesh, self.lower_mesh, *self.design_meshes]:
            if Path(mesh).suffix.lower() not in {".stl", ".ply", ".obj"}:
                raise ValueError(f"Unsupported mesh: {mesh}")

    def save(self, path: str | Path) -> None:
        self.validate_extensions()
        Path(path).write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
