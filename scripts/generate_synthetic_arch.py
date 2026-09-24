from argparse import ArgumentParser
from src.dental.synthetic_arch import write_obj


def main():
    p = ArgumentParser()
    p.add_argument("--out", default="outputs/synthetic_maxillary_arch.obj")
    args = p.parse_args()
    path = write_obj(args.out)
    print(path)


if __name__ == "__main__":
    main()
