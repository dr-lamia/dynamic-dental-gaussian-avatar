import json
import numpy as np
from pathlib import Path
from src.dental.teeth3ds import load_case, select_teeth


def test_teeth3ds_loader(tmp_path: Path):
    obj = tmp_path / "case.obj"
    obj.write_text(
        "v 0 0 0\n"
        "v 1 0 0\n"
        "v 0 1 0\n"
        "v 1 1 0\n"
        "f 1 2 3\n"
        "f 2 4 3\n",
        encoding="utf-8",
    )
    meta = {
        "id_patient": "DEMO",
        "jaw": "upper",
        "labels": [11, 11, 21, 21],
        "instances": [1, 1, 2, 2],
    }
    js = tmp_path / "case.json"
    js.write_text(json.dumps(meta), encoding="utf-8")

    case = load_case(obj, js)
    assert case.patient_id == "DEMO"
    assert case.jaw == "upper"
    assert case.tooth_labels == [11, 21]


def test_select_teeth(tmp_path: Path):
    obj = tmp_path / "case.obj"
    obj.write_text(
        "v 0 0 0\n"
        "v 1 0 0\n"
        "v 0 1 0\n"
        "v 1 1 0\n"
        "f 1 2 3\n"
        "f 2 4 3\n",
        encoding="utf-8",
    )
    meta = {
        "id_patient": "DEMO",
        "jaw": "upper",
        "labels": [11, 11, 11, 21],
        "instances": [1, 1, 1, 2],
    }
    js = tmp_path / "case.json"
    js.write_text(json.dumps(meta), encoding="utf-8")

    case = load_case(obj, js)
    v, f = select_teeth(case, [11])
    assert len(v) == 3
    assert len(f) == 1
