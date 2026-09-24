"""Apply a saved manual alignment to a Teeth3DS mesh and export aligned OBJ."""
from argparse import ArgumentParser

from src.dental.teeth3ds import load_case, select_teeth
from src.dental.design_swap import save_obj
from src.registration.manual_alignment import ManualAlignment


def main():
    p = ArgumentParser()
    p.add_argument("--obj", required=True)
    p.add_argument("--json", required=True)
    p.add_argument("--alignment", required=True)
    p.add_argument("--teeth", nargs="*", type=int, default=[13,12,11,21,22,23])
    p.add_argument("--out", default="outputs/aligned_teeth3ds.obj")
    a = p.parse_args()

    case = load_case(a.obj, a.json)
    verts, faces = select_teeth(case, a.teeth)
    alignment = ManualAlignment.load(a.alignment)
    verts_aligned = alignment.apply(verts)
    save_obj(a.out, verts_aligned, faces)
    print(a.out)


if __name__ == "__main__":
    main()
