"""Standalone MultiFace subset inspector for Windows/PowerShell.

No project imports are required. Uses Python standard library only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


EXPRESSIONS = [
    "E001_Neutral_Eyes_Open",
    "E009_Smile_Mouth_Open",
    "E029_Show_All_Teeth",
]

_FLOAT_RE = re.compile(
    r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
)


def load_headpose_matrix(path: Path):
    """Parse MultiFace head-pose text robustly.

    Accepts whitespace, comma/bracket formatted 4x4 matrices, and 3x4 matrices.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    values = [float(x) for x in _FLOAT_RE.findall(text)]

    if len(values) >= 16:
        values = values[:16]
        return [values[i:i + 4] for i in range(0, 16, 4)]

    if len(values) >= 12:
        values = values[:12]
        rows = [values[i:i + 4] for i in range(0, 12, 4)]
        rows.append([0.0, 0.0, 0.0, 1.0])
        return rows

    preview = text[:300].replace("\n", " | ")
    raise ValueError(
        f"Could not parse transform from {path}. "
        f"Found only {len(values)} numeric values. File preview: {preview}"
    )


def inspect(root: Path):
    report = {
        "root": str(root.resolve()),
        "expressions": {},
        "total_frames": 0,
    }

    for expression in EXPRESSIONS:
        folder = root / "tracked_mesh" / expression
        if not folder.is_dir():
            report["expressions"][expression] = {
                "present": False,
                "frames": 0,
            }
            continue

        objs = sorted(folder.glob("*.obj"))
        paired = []
        missing_transforms = []

        for obj in objs:
            frame_id = obj.stem
            transform = folder / f"{frame_id}_transform.txt"
            if transform.exists():
                paired.append((frame_id, obj, transform))
            else:
                missing_transforms.append(frame_id)

        info = {
            "present": True,
            "obj_files": len(objs),
            "paired_frames": len(paired),
            "missing_transform_count": len(missing_transforms),
            "first_frame": paired[0][0] if paired else None,
            "last_frame": paired[-1][0] if paired else None,
        }

        if paired:
            info["first_headpose_matrix"] = load_headpose_matrix(paired[0][2])

        report["expressions"][expression] = info
        report["total_frames"] += len(paired)

    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("multiface_root")
    parser.add_argument("--out")
    args = parser.parse_args()

    root = Path(args.multiface_root)
    if not root.is_dir():
        raise SystemExit(f"Folder not found: {root}")

    report = inspect(root)
    text = json.dumps(report, indent=2)
    print(text)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Saved report: {out}")


if __name__ == "__main__":
    main()
