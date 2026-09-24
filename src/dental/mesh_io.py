"""Dental mesh I/O utilities.

Keep metric coordinates unchanged on load. Real patient data should live outside Git.
"""
from pathlib import Path


def validate_mesh_path(path: str | Path) -> Path:
    p = Path(path)
    if p.suffix.lower() not in {".stl", ".ply", ".obj"}:
        raise ValueError(f"Unsupported dental mesh format: {p.suffix}")
    return p
