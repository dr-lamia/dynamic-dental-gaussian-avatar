"""Validate a real-patient case before running the 4D pipeline."""
from __future__ import annotations

from argparse import ArgumentParser
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analytics.jaw_motion_metrics import summarize_jaw_motion
from src.dental.case_manifest import CaseManifest
from src.dental.jaw_motion import load_jaw_motion_csv


def validate_case(manifest_path: str | Path) -> dict:
    manifest_path = Path(manifest_path).resolve()
    manifest = CaseManifest.load(manifest_path)
    resolved = manifest.resolve_files(manifest_path)

    file_checks = {}
    missing = []
    for key, path in resolved.items():
        exists = path.is_file()
        file_checks[key] = {
            "path": str(path),
            "exists": exists,
            "size_bytes": path.stat().st_size if exists else None,
        }
        if not exists:
            missing.append(key)

    report = {
        "case_id": manifest.case_id,
        "manifest": str(manifest_path),
        "ready": len(missing) == 0,
        "missing": missing,
        "files": file_checks,
        "jaw_motion": None,
    }

    jaw_path = resolved.get("jaw_motion_csv")
    if jaw_path is not None and jaw_path.is_file():
        sequence = load_jaw_motion_csv(jaw_path)
        report["jaw_motion"] = summarize_jaw_motion(sequence)

    return report


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("manifest", help="Path to the patient case JSON manifest")
    parser.add_argument("--report", help="Optional path for a JSON validation report")
    args = parser.parse_args()

    report = validate_case(args.manifest)
    text = json.dumps(report, indent=2)
    print(text)

    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Saved validation report: {out}")

    if not report["ready"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
