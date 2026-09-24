"""Alignment session metadata for auditability/reproducibility."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json


@dataclass
class AlignmentSession:
    face_sequence: str
    dental_case_id: str
    dental_source: str
    reference_frame: int
    alignment_file: str
    notes: str = ""

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
        return path
