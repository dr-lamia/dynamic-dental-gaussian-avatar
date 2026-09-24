"""Find a usable local Teeth3DS case without hard-coding a patient ID."""
from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path
import json


def discover(root: Path, jaw: str):
    objs = sorted(root.rglob(f"*_{jaw}.obj"))
    for obj in objs:
        stem = obj.stem
        patient = stem[: -(len(jaw) + 1)]
        candidates = [
            obj.with_suffix(".json"),
            root / "ground-truth_labels_instances" / patient / f"{stem}.json",
            obj.parent.parent.parent / "ground-truth_labels_instances" / patient / f"{stem}.json",
        ]
        js = next((p for p in candidates if p.exists()), None)
        if js is not None:
            yield obj, js


def main():
    p = ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--jaw", choices=["upper", "lower"], default="upper")
    p.add_argument("--out", default="outputs/selected_teeth3ds_case.json")
    a = p.parse_args()

    root = Path(a.root)
    found = next(discover(root, a.jaw), None)
    if found is None:
        raise SystemExit(f"No paired {a.jaw} OBJ+JSON case found under {root}")

    obj, js = found
    meta = json.loads(js.read_text(encoding="utf-8"))
    result = {
        "patient_id": meta.get("id_patient"),
        "jaw": meta.get("jaw"),
        "obj": str(obj.resolve()),
        "json": str(js.resolve()),
    }

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
