"""Simple 2D wireframe preview for dental alignment debugging."""
from __future__ import annotations
import numpy as np

from src.rendering.projection import project_points


def projected_edges(
    vertices_world: np.ndarray,
    faces: np.ndarray,
    world_to_camera: np.ndarray,
    K: np.ndarray,
):
    uv = project_points(vertices_world, world_to_camera, K)
    edges = set()
    for tri in np.asarray(faces, int):
        a,b,c = [int(x) for x in tri]
        for u,v in ((a,b),(b,c),(c,a)):
            edges.add(tuple(sorted((u,v))))
    return uv, sorted(edges)


def overlay_wireframe(
    image: np.ndarray,
    uv: np.ndarray,
    edges: list[tuple[int,int]],
    line_value=255,
) -> np.ndarray:
    """Rasterize thin lines with a basic interpolation, dependency-free."""
    img = np.array(image, copy=True)
    h,w = img.shape[:2]

    def draw(p0,p1):
        x0,y0 = p0
        x1,y1 = p1
        n = max(1, int(max(abs(x1-x0), abs(y1-y0))) + 1)
        xs = np.linspace(x0,x1,n)
        ys = np.linspace(y0,y1,n)
        xi = np.round(xs).astype(int)
        yi = np.round(ys).astype(int)
        valid = (xi>=0)&(xi<w)&(yi>=0)&(yi<h)
        if img.ndim == 2:
            img[yi[valid],xi[valid]] = line_value
        else:
            img[yi[valid],xi[valid],:] = line_value

    for a,b in edges:
        draw(uv[a], uv[b])
    return img
