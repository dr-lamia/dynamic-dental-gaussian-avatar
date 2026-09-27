"""Create a local patient-case manifest without copying patient data into Git."""
from argparse import ArgumentParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.dental.case_manifest import CaseManifest


def main() -> None:
    p = ArgumentParser()
    p.add_argument("--case-id", required=True)
    p.add_argument("--video", required=True)
    p.add_argument("--upper", required=True)
    p.add_argument("--lower", required=True)
    p.add_argument("--design", action="append", required=True)
    p.add_argument("--bite")
    p.add_argument("--jaw-motion", help="Standardized jaw-motion CSV")
    p.add_argument("--out", default="data/local_case.json")
    a = p.parse_args()

    manifest = CaseManifest(
        case_id=a.case_id,
        video=a.video,
        upper_mesh=a.upper,
        lower_mesh=a.lower,
        design_meshes=a.design,
        bite_mesh=a.bite,
        jaw_motion_csv=a.jaw_motion,
    )
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest.save(out)
    print(f"Saved case manifest: {out}")


if __name__ == "__main__":
    main()
