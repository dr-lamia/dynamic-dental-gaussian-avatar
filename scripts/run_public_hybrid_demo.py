"""Orchestrate the public hybrid avatar+dental demo.

This script deliberately separates GPU execution (VHAP/GaussianAvatars) from
our dental preprocessing. It can emit a complete execution plan even on a
machine where the GPU backends are not installed.
"""
from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path
import json
import subprocess

from src.dental.teeth3ds import load_case, select_teeth
from src.dental.design_swap import save_obj


def main():
    p = ArgumentParser()
    p.add_argument("--vhap-repo", required=True)
    p.add_argument("--gaussian-repo", required=True)
    p.add_argument("--public-video", required=True)
    p.add_argument("--teeth-obj", required=True)
    p.add_argument("--teeth-json", required=True)
    p.add_argument("--work-dir", default="outputs/public_hybrid_demo")
    p.add_argument("--execute-dental", action="store_true")
    a = p.parse_args()

    work = Path(a.work_dir)
    work.mkdir(parents=True, exist_ok=True)

    case = load_case(a.teeth_obj, a.teeth_json)
    if case.jaw.lower() != "upper":
        raise ValueError("First public hybrid demo requires an upper-jaw Teeth3DS case")

    selected = [13, 12, 11, 21, 22, 23]
    available = set(case.tooth_labels)
    selected = [x for x in selected if x in available]
    if not selected:
        raise ValueError("No maxillary anterior FDI teeth (13–23) available in selected case")

    dental_out = work / "teeth3ds_anterior.obj"
    if a.execute_dental:
        v, f = select_teeth(case, selected)
        save_obj(dental_out, v, f)

    video = Path(a.public_video)
    sequence = video.stem
    vhap_export = Path(a.vhap_repo) / "export" / "monocular" / f"{sequence}_whiteBg_staticOffset_maskBelowLine"
    gaussian_model = Path(a.gaussian_repo) / "output" / f"dental_virtual_patient_{sequence}"

    plan = {
        "inputs": {
            "public_video": str(video),
            "teeth3ds_patient_id": case.patient_id,
            "teeth3ds_upper_obj": str(Path(a.teeth_obj)),
            "teeth3ds_labels_json": str(Path(a.teeth_json)),
            "selected_fdi": selected,
        },
        "dental_output": str(dental_out),
        "vhap": {
            "repo": str(Path(a.vhap_repo)),
            "expected_export": str(vhap_export),
            "command": f"/path/to/project/scripts/public_vhap_demo.sh {video.name}",
        },
        "gaussian_avatars": {
            "repo": str(Path(a.gaussian_repo)),
            "model_output": str(gaussian_model),
            "command": f"/path/to/project/scripts/public_gaussian_avatar_demo.sh {vhap_export} {gaussian_model}",
        },
        "next_hybrid_step": {
            "register": "estimate T_upper_to_face from corresponding landmarks",
            "occlusion": "project VHAP FLAME lip rings and depth-test dental pixels",
            "validation": "compute relative dental-to-facial temporal drift in mm",
        },
    }

    (work / "execution_plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
