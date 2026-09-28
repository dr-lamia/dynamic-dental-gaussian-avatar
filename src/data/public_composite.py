"""Provenance model for a composite public-data 4D benchmark.

A composite benchmark intentionally combines modules from different public
datasets for engineering development. It must never be represented as a
patient-specific digital twin.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import yaml


ALLOWED_CLAIM_LEVEL = "engineering_benchmark_not_patient_specific"


@dataclass(frozen=True)
class PublicComponent:
    role: str
    source_name: str
    source_url: str
    local_path: str | None = None
    source_subject_or_case_id: str | None = None
    license: str | None = None
    notes: str | None = None


@dataclass
class PublicCompositeManifest:
    benchmark_id: str
    claim_level: str
    components: list[PublicComponent]

    def validate(self) -> None:
        if self.claim_level != ALLOWED_CLAIM_LEVEL:
            raise ValueError(
                "Public composite data must use claim_level="
                f"{ALLOWED_CLAIM_LEVEL!r}"
            )
        if len(self.components) < 2:
            raise ValueError("A composite benchmark needs at least two components")
        roles = [c.role for c in self.components]
        if len(set(roles)) != len(roles):
            raise ValueError("Component roles must be unique")
        for component in self.components:
            if not component.source_name.strip():
                raise ValueError("source_name cannot be empty")
            if not component.source_url.startswith(("http://", "https://")):
                raise ValueError("source_url must be HTTP(S)")

    def save(self, path: str | Path) -> None:
        self.validate()
        Path(path).write_text(
            json.dumps(
                {
                    "benchmark_id": self.benchmark_id,
                    "claim_level": self.claim_level,
                    "components": [asdict(c) for c in self.components],
                },
                indent=2,
            ),
            encoding="utf-8",
        )


def load_benchmark_config(path: str | Path) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if data.get("claim_level") != ALLOWED_CLAIM_LEVEL:
        raise ValueError("Config is not labeled as a non-patient-specific benchmark")
    return data
