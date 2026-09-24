"""Create/save an explicit manual dental-to-face alignment file."""
from argparse import ArgumentParser
from src.registration.manual_alignment import ManualAlignment


def main():
    p = ArgumentParser()
    p.add_argument("--tx", type=float, default=0.0)
    p.add_argument("--ty", type=float, default=0.0)
    p.add_argument("--tz", type=float, default=0.0)
    p.add_argument("--rx", type=float, default=0.0)
    p.add_argument("--ry", type=float, default=0.0)
    p.add_argument("--rz", type=float, default=0.0)
    p.add_argument("--out", default="outputs/manual_alignment.json")
    a = p.parse_args()

    alignment = ManualAlignment(
        translation_mm=(a.tx, a.ty, a.tz),
        rotation_deg_xyz=(a.rx, a.ry, a.rz),
    )
    print(alignment.save(a.out))


if __name__ == "__main__":
    main()
