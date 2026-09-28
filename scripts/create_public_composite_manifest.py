"""Create a provenance-safe manifest for a public composite 4D benchmark."""
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.public_composite import (
    ALLOWED_CLAIM_LEVEL,
    PublicComponent,
    PublicCompositeManifest,
    load_benchmark_config,
)


def _component_from_config(role: str, data: dict, local_path: str | None, source_id: str | None):
    return PublicComponent(
        role=role,
        source_name=data["source_name"],
        source_url=data["source_url"],
        local_path=local_path,
        source_subject_or_case_id=source_id,
        license=data.get("license"),
        notes=data.get("use") or data.get("license_note"),
    )


def main() -> None:
    p = ArgumentParser()
    p.add_argument(
        "--config",
        default="configs/public_composite_benchmark.yaml",
        help="Public benchmark YAML configuration",
    )
    p.add_argument("--dental-path")
    p.add_argument("--dental-id")
    p.add_argument("--face-path")
    p.add_argument("--face-id")
    p.add_argument("--jaw-path")
    p.add_argument("--jaw-id")
    p.add_argument(
        "--out",
        default="data/public_composite_manifest.json",
        help="Output JSON manifest",
    )
    args = p.parse_args()

    cfg = load_benchmark_config(args.config)
    components = [
        _component_from_config(
            "dental",
            cfg["components"]["dental"],
            args.dental_path,
            args.dental_id,
        ),
        _component_from_config(
            "face_motion",
            cfg["components"]["face_motion"],
            args.face_path,
            args.face_id,
        ),
        _component_from_config(
            "jaw_motion_engineering",
            cfg["components"]["jaw_motion_engineering"],
            args.jaw_path,
            args.jaw_id,
        ),
    ]

    manifest = PublicCompositeManifest(
        benchmark_id=cfg["benchmark_id"],
        claim_level=ALLOWED_CLAIM_LEVEL,
        components=components,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest.save(out)
    print(f"Saved public composite manifest: {out}")


if __name__ == "__main__":
    main()
