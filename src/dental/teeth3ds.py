"""Teeth3DS / 3DTeethSeg loader.

The dataset provides an OBJ mesh and a JSON file containing one FDI label and
one instance id per mesh vertex. This module reads those files without
redistributing the dataset.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import numpy as np


@dataclass
class Teeth3DSCase:
    patient_id: str
    jaw: str
    vertices: np.ndarray
    faces: np.ndarray
    labels: np.ndarray
    instances: np.ndarray

    @property
    def tooth_labels(self) -> list[int]:
        return sorted(int(x) for x in np.unique(self.labels) if int(x) != 0)


def read_obj(path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    vertices = []
    faces = []
    with Path(path).open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("v "):
                parts = line.split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith("f "):
                parts = line.split()[1:4]
                idx = [int(p.split("/")[0]) - 1 for p in parts]
                faces.append(idx)
    return np.asarray(vertices, float), np.asarray(faces, int)


def load_case(obj_path: str | Path, json_path: str | Path) -> Teeth3DSCase:
    vertices, faces = read_obj(obj_path)
    meta = json.loads(Path(json_path).read_text(encoding="utf-8"))
    labels = np.asarray(meta["labels"], dtype=int)
    instances = np.asarray(meta["instances"], dtype=int)

    if len(vertices) != len(labels) or len(vertices) != len(instances):
        raise ValueError("Teeth3DS vertex count does not match JSON labels/instances")

    return Teeth3DSCase(
        patient_id=str(meta["id_patient"]),
        jaw=str(meta["jaw"]),
        vertices=vertices,
        faces=faces,
        labels=labels,
        instances=instances,
    )


def select_teeth(case: Teeth3DSCase, fdi_labels: list[int]) -> tuple[np.ndarray, np.ndarray]:
    """Return a compact submesh containing only selected FDI teeth."""
    keep_vertex = np.isin(case.labels, np.asarray(fdi_labels, dtype=int))
    keep_face = np.all(keep_vertex[case.faces], axis=1)
    faces_old = case.faces[keep_face]

    old_ids = np.flatnonzero(keep_vertex)
    remap = -np.ones(len(case.vertices), dtype=int)
    remap[old_ids] = np.arange(len(old_ids))
    faces_new = remap[faces_old]
    vertices_new = case.vertices[old_ids]
    return vertices_new, faces_new
