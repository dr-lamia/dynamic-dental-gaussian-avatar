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

    @classmethod
    def load(cls, path: str | Path) -> "CaseManifest":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        manifest = cls(**data)
        manifest.validate_extensions()
        return manifest

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

        if not self.design_meshes:
            raise ValueError("At least one design mesh is required")

        if self.jaw_motion_csv and Path(self.jaw_motion_csv).suffix.lower() != ".csv":
            raise ValueError("jaw_motion_csv must be a .csv file")

    def referenced_files(self) -> dict[str, str]:
        files = {
            "video": self.video,
            "upper_mesh": self.upper_mesh,
            "lower_mesh": self.lower_mesh,
        }
        if self.bite_mesh:
            files["bite_mesh"] = self.bite_mesh
        if self.jaw_motion_csv:
            files["jaw_motion_csv"] = self.jaw_motion_csv
        for i, mesh in enumerate(self.design_meshes, start=1):
            files[f"design_mesh_{i}"] = mesh
        return files

    def resolve_files(self, manifest_path: str | Path) -> dict[str, Path]:
        base = Path(manifest_path).resolve().parent
        resolved: dict[str, Path] = {}
        for key, value in self.referenced_files().items():
            p = Path(value).expanduser()
            if not p.is_absolute():
                p = base / p
            resolved[key] = p.resolve()
        return resolved

    def save(self, path: str | Path) -> None:
        self.validate_extensions()
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
