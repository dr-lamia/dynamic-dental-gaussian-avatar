"""Inspect the downloaded minimal MultiFace dental subset."""
from __future__ import annotations

from argparse import ArgumentParser
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tracking.multiface import discover_dental_subset, load_headpose_matrix


def main() -> None:
    p = ArgumentParser()
    p.add_argument(
        "multiface_root",
        help=(
            "Path to the MultiFace identity root containing tracked_mesh, e.g. "
            r"D:\MultiFace-dental-minimal\m--20180227--0000--6795937--GHS"
        ),
    )
    p.add_argument("--out", default=None, help="Optional JSON report")
    args = p.parse_args()

    root = Path(args.multiface_root)
    sequences = discover_dental_subset(root)

    report = {
        "root": str(root.resolve()),
        "expressions": {},
        "total_frames": 0,
    }

    for expression, sequence in sequences.items():
        first = sequence.frames[0]
        matrix = load_headpose_matrix(first.transform_path)
        report["expressions"][expression] = {
            "frames": len(sequence.frames),
            "first_frame": first.frame_id,
            "last_frame": sequence.frames[-1].frame_id,
            "first_headpose_matrix": matrix.tolist(),
        }
        report["total_frames"] += len(sequence.frames)

    text = json.dumps(report, indent=2)
    print(text)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Saved report: {out}")


if __name__ == "__main__":
    main()
