"""Procedural synthetic dental arches for public engineering tests.

These meshes are intentionally schematic, not clinically realistic. They give
the registration/rendering pipeline reproducible geometry without patient data
or third-party dataset redistribution.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import math
import numpy as np


@dataclass(frozen=True)
class ToothSpec:
    fdi: int
    center: tuple[float, float, float]
    radii: tuple[float, float, float]


def _ellipsoid(center, radii, n_theta=18, n_phi=10):
    cx, cy, cz = center
    rx, ry, rz = radii
    verts = []
    faces = []
    for i in range(n_phi + 1):
        phi = math.pi * i / n_phi
        for j in range(n_theta):
            th = 2 * math.pi * j / n_theta
            x = cx + rx * math.sin(phi) * math.cos(th)
            y = cy + ry * math.sin(phi) * math.sin(th)
            z = cz + rz * math.cos(phi)
            verts.append((x, y, z))
    for i in range(n_phi):
        for j in range(n_theta):
            a = i * n_theta + j
            b = i * n_theta + (j + 1) % n_theta
            c = (i + 1) * n_theta + j
            d = (i + 1) * n_theta + (j + 1) % n_theta
            faces.append((a, c, b))
            faces.append((b, c, d))
    return np.asarray(verts, float), np.asarray(faces, int)


def _radii_for_tooth_index(k: int, mandibular: bool = False) -> tuple[float, float, float]:
    if k == 0:
        radii = (4.2, 3.8, 5.3)
    elif k == 1:
        radii = (3.4, 3.2, 5.0)
    elif k == 2:
        radii = (3.6, 3.8, 5.4)
    elif k in (3, 4):
        radii = (4.2, 4.8, 4.6)
    else:
        radii = (5.0, 5.8, 4.4)
    if mandibular:
        radii = (radii[0] * 0.94, radii[1] * 0.94, radii[2] * 0.90)
    return radii


def default_maxillary_specs() -> list[ToothSpec]:
    """Create 14 schematic maxillary teeth (17→27, excluding third molars)."""
    specs = []
    fdis = [17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27]
    for idx, fdi in enumerate(fdis):
        side = -1 if idx < 7 else 1
        k = idx if idx < 7 else 13 - idx
        x = side * (5.0 + 5.1 * k)
        y = 21.0 - 2.2 * (k ** 1.55)
        specs.append(ToothSpec(fdi=fdi, center=(x, y, 0.0), radii=_radii_for_tooth_index(k)))
    return specs


def default_mandibular_specs() -> list[ToothSpec]:
    """Create 14 schematic mandibular teeth (47→37, excluding third molars)."""
    specs = []
    fdis = [47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37]
    for idx, fdi in enumerate(fdis):
        side = -1 if idx < 7 else 1
        k = idx if idx < 7 else 13 - idx
        x = side * (4.6 + 4.9 * k)
        y = 18.0 - 2.0 * (k ** 1.52)
        specs.append(
            ToothSpec(
                fdi=fdi,
                center=(x, y, 0.0),
                radii=_radii_for_tooth_index(k, mandibular=True),
            )
        )
    return specs


def _build_arch(specs: list[ToothSpec]):
    vertices = []
    faces = []
    labels = []
    offset = 0
    for spec in specs:
        v, f = _ellipsoid(spec.center, spec.radii)
        vertices.append(v)
        faces.append(f + offset)
        labels.extend([spec.fdi] * len(v))
        offset += len(v)
    return np.vstack(vertices), np.vstack(faces), np.asarray(labels, int)


def build_maxillary_arch():
    return _build_arch(default_maxillary_specs())


def build_mandibular_arch():
    return _build_arch(default_mandibular_specs())


def _write_arch_obj(path: str | Path, builder, arch_name: str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    verts, faces, labels = builder()
    with path.open("w", encoding="utf-8") as f:
        f.write(f"# Synthetic {arch_name} arch for engineering tests only\n")
        last_label = None
        for label, v in zip(labels, verts):
            if label != last_label:
                f.write(f"# FDI {label}\n")
                last_label = label
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        for tri in faces:
            a, b, c = tri + 1
            f.write(f"f {a} {b} {c}\n")
    return path


def write_obj(path: str | Path) -> Path:
    """Backward-compatible maxillary synthetic OBJ writer."""
    return _write_arch_obj(path, build_maxillary_arch, "maxillary")


def write_mandibular_obj(path: str | Path) -> Path:
    return _write_arch_obj(path, build_mandibular_arch, "mandibular")
