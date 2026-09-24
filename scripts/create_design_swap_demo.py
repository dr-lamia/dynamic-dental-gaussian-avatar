"""Generate two synthetic smile states with an identical maxillary motion chain."""
from pathlib import Path
import numpy as np

from src.dental.synthetic_arch import build_maxillary_arch
from src.dental.design_swap import transform_design_to_world, save_obj


def main():
    vertices, faces, labels = build_maxillary_arch()

    original = vertices.copy()
    design = vertices.copy()

    # Engineering-only "veneer effect": slightly lengthen anterior teeth.
    anterior = np.isin(labels, [13, 12, 11, 21, 22, 23])
    design[anterior, 2] -= 1.2

    I = np.eye(4)
    face_to_world = np.eye(4)
    face_to_world[:3, 3] = [0.0, 0.0, 100.0]

    out = Path("outputs/design_swap_demo")
    save_obj(out / "original.obj", transform_design_to_world(original, I, I, face_to_world), faces)
    save_obj(out / "design_a.obj", transform_design_to_world(design, I, I, face_to_world), faces)
    print(out)


if __name__ == "__main__":
    main()
