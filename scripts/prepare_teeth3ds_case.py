"""Prepare a local Teeth3DS scan for the dynamic-avatar pipeline."""
from argparse import ArgumentParser
from pathlib import Path
import json

from src.dental.teeth3ds import load_case, select_teeth
from src.dental.design_swap import save_obj


def main():
    p = ArgumentParser()
    p.add_argument("--obj", required=True)
    p.add_argument("--json", required=True)
    p.add_argument("--teeth", nargs="*", type=int, default=[13,12,11,21,22,23])
    p.add_argument("--out-dir", default="outputs/teeth3ds_case")
    a = p.parse_args()

    case = load_case(a.obj, a.json)
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    v, f = select_teeth(case, a.teeth)
    save_obj(out / "selected_teeth.obj", v, f)

    summary = {
        "patient_id": case.patient_id,
        "jaw": case.jaw,
        "available_fdi_labels": case.tooth_labels,
        "selected_fdi_labels": a.teeth,
        "n_vertices_full": int(len(case.vertices)),
        "n_faces_full": int(len(case.faces)),
        "n_vertices_selected": int(len(v)),
        "n_faces_selected": int(len(f)),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
