"""Render a simple 2D wireframe preview from dental OBJ + alignment JSON."""
from argparse import ArgumentParser
from pathlib import Path
import numpy as np

from src.dental.teeth3ds import read_obj
from src.registration.manual_alignment import ManualAlignment
from src.rendering.wireframe_preview import projected_edges, overlay_wireframe


def main():
    p = ArgumentParser()
    p.add_argument("--obj", required=True)
    p.add_argument("--alignment", required=True)
    p.add_argument("--width", type=int, default=800)
    p.add_argument("--height", type=int, default=800)
    p.add_argument("--fx", type=float, default=700.0)
    p.add_argument("--fy", type=float, default=700.0)
    p.add_argument("--out", default="outputs/alignment_preview.npy")
    a = p.parse_args()

    v,f = read_obj(a.obj)
    alignment = ManualAlignment.load(a.alignment)
    vw = alignment.apply(v)

    K = np.array([
        [a.fx, 0, a.width/2],
        [0, a.fy, a.height/2],
        [0, 0, 1],
    ], float)
    W2C = np.eye(4, dtype=float)

    uv, edges = projected_edges(vw, f, W2C, K)
    canvas = np.zeros((a.height,a.width,3), dtype=np.uint8)
    preview = overlay_wireframe(canvas, uv, edges)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.save(out, preview)
    print(out)


if __name__ == "__main__":
    main()
