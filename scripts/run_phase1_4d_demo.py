"""Run a fully public/synthetic Phase-1 4D dental motion demo.

No patient data or third-party datasets are required. The script uses schematic
upper/lower arches and a standardized jaw-motion CSV, then exports every frame
plus quantitative motion metrics.
"""
from __future__ import annotations

from argparse import ArgumentParser
import csv
import json
from pathlib import Path
import numpy as np

from src.analytics.jaw_motion_metrics import (
    displacement_from_start_mm,
    rotation_from_start_deg,
    summarize_jaw_motion,
)
from src.dental.design_swap import save_obj
from src.dental.jaw_motion import load_jaw_motion_csv
from src.dental.motion import lower_vertices_for_frame, upper_vertices_for_frame
from src.dental.synthetic_arch import build_mandibular_arch, build_maxillary_arch


def _design_variant(vertices: np.ndarray, labels: np.ndarray) -> np.ndarray:
    design = vertices.copy()
    anterior = np.isin(labels, [13, 12, 11, 21, 22, 23])
    design[anterior, 2] -= 1.2
    return design


def run_demo(jaw_motion_csv: str | Path, out_dir: str | Path) -> dict:
    sequence = load_jaw_motion_csv(jaw_motion_csv)
    out = Path(out_dir)
    frames_dir = out / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    upper_v, upper_f, upper_labels = build_maxillary_arch()
    lower_v, lower_f, _ = build_mandibular_arch()
    design_v = _design_variant(upper_v, upper_labels)

    upper_to_face = np.eye(4)
    lower_to_mandible = np.eye(4)

    # Synthetic static registration only: separate the lower arch from the upper.
    # A real case obtains this transform from patient-specific bite/registration.
    lower_to_mandible[:3, 3] = [0.0, -1.0, -12.0]

    displacement = displacement_from_start_mm(sequence)
    rotation = rotation_from_start_deg(sequence)
    trajectory_rows = []

    for i, sample in enumerate(sequence.samples):
        frame = sequence.to_frame_state(sample.frame_index)

        upper_world = upper_vertices_for_frame(upper_v, upper_to_face, frame)
        design_world = upper_vertices_for_frame(design_v, upper_to_face, frame)
        lower_world = lower_vertices_for_frame(lower_v, lower_to_mandible, frame)

        prefix = frames_dir / f"frame_{sample.frame_index:04d}"
        save_obj(prefix.with_name(prefix.name + "_upper.obj"), upper_world, upper_f)
        save_obj(prefix.with_name(prefix.name + "_lower.obj"), lower_world, lower_f)
        save_obj(prefix.with_name(prefix.name + "_design_a.obj"), design_world, upper_f)

        lower_centroid = lower_world.mean(axis=0)
        jaw_translation = sample.mandible_to_face[:3, 3]
        trajectory_rows.append(
            {
                "frame_index": sample.frame_index,
                "timestamp_s": "" if sample.timestamp_s is None else sample.timestamp_s,
                "jaw_tx_mm": float(jaw_translation[0]),
                "jaw_ty_mm": float(jaw_translation[1]),
                "jaw_tz_mm": float(jaw_translation[2]),
                "displacement_from_start_mm": float(displacement[i]),
                "rotation_from_start_deg": float(rotation[i]),
                "jaw_opening_mm": "" if sample.jaw_opening_mm is None else sample.jaw_opening_mm,
                "lower_centroid_x_mm": float(lower_centroid[0]),
                "lower_centroid_y_mm": float(lower_centroid[1]),
                "lower_centroid_z_mm": float(lower_centroid[2]),
            }
        )

    metrics = summarize_jaw_motion(sequence)
    metrics["synthetic_demo"] = True
    metrics["source_jaw_motion_csv"] = str(jaw_motion_csv)

    (out / "metrics.json").write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    fields = list(trajectory_rows[0])
    with (out / "trajectory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(trajectory_rows)

    summary = f"""# Phase-1 4D Dental Motion Demo

This output uses **synthetic dental arches** and is for engineering validation only.

- Frames: {metrics['frames']}
- Duration: {metrics['duration_s']} s
- Translational path length: {metrics['path_length_mm']:.3f} mm
- Maximum displacement from start: {metrics['max_displacement_from_start_mm']:.3f} mm
- Maximum rotation from start: {metrics['max_rotation_from_start_deg']:.3f}°
- Maximum supplied jaw opening: {metrics['max_jaw_opening_mm']} mm

Each frame contains:
- maxillary/original dentition OBJ
- mandibular OBJ driven by the jaw-motion transform
- maxillary Design A OBJ driven by exactly the same head/maxillary transform

For a real patient, replace the synthetic arches, static lower registration and example
motion CSV with patient-specific IOS, bite registration and synchronized jaw tracking.
"""
    (out / "SUMMARY.md").write_text(summary, encoding="utf-8")
    return metrics


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--jaw-motion",
        default="examples/jaw_motion.example.csv",
        help="Standardized jaw-motion CSV",
    )
    parser.add_argument(
        "--out",
        default="outputs/phase1_4d_demo",
        help="Output directory",
    )
    args = parser.parse_args()

    metrics = run_demo(args.jaw_motion, args.out)
    print(json.dumps(metrics, indent=2))
    print(f"Outputs written to: {args.out}")


if __name__ == "__main__":
    main()
