"""Recover exocad crown-export transforms from constructionInfo XML.

exocad XML matrices observed in this project use a row-vector homogeneous
convention: [x, y, z, 1] @ M.

For construction exports marked RotateToAxisInsertion, the exported crown STL
can be mapped back to scan coordinates with:

    crown_scan = crown_export
                 @ inverse(ZRotationMatrix)
                 @ inverse(MatrixToScanDataFiles)

For exports without that additional rotation, the scan mapping is simply
inverse(MatrixToScanDataFiles).

Always validate the recovered placement against the corresponding IOS/tooth
model because vendor/export settings may differ between software versions.
"""
from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np


def _read_row_matrix(node: ET.Element | None) -> np.ndarray:
    if node is None:
        raise ValueError("Required matrix is missing from constructionInfo XML")
    M = np.zeros((4, 4), dtype=float)
    for i in range(4):
        for j in range(4):
            text = node.findtext(f"_{i}{j}")
            if text is None:
                raise ValueError(f"Matrix entry _{i}{j} is missing")
            M[i, j] = float(text)
    return M


def find_construction_file(
    construction_info_path: str | Path,
    tooth_fdi: int,
) -> ET.Element:
    root = ET.parse(construction_info_path).getroot()
    matches = []
    for item in root.findall(".//ConstructionFile"):
        tooth_numbers = [
            int(x.text)
            for x in item.findall("./ToothNumbers/int")
            if x.text is not None
        ]
        if int(tooth_fdi) in tooth_numbers:
            matches.append(item)

    if not matches:
        raise ValueError(f"No construction file found for tooth {tooth_fdi}")
    if len(matches) > 1:
        raise ValueError(
            f"Multiple construction files found for tooth {tooth_fdi}; "
            "select the intended export explicitly before alignment"
        )
    return matches[0]


def crown_export_to_scan_transform(
    construction_info_path: str | Path,
    tooth_fdi: int,
) -> np.ndarray:
    """Return the row-vector transform mapping exported crown STL -> scan space."""
    item = find_construction_file(construction_info_path, tooth_fdi)
    scan_matrix = _read_row_matrix(item.find("MatrixToScanDataFiles"))
    transform = np.linalg.inv(scan_matrix)

    export_information = (item.findtext("ExportInformation") or "").strip()
    z_node = item.find("ZRotationMatrix")
    if "RotateToAxisInsertion" in export_information:
        if z_node is None:
            raise ValueError(
                "ExportInformation indicates RotateToAxisInsertion but "
                "ZRotationMatrix is missing"
            )
        z_matrix = _read_row_matrix(z_node)
        transform = np.linalg.inv(z_matrix) @ transform

    return transform


def apply_row_transform(points: np.ndarray, transform: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    transform = np.asarray(transform, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must be Nx3")
    if transform.shape != (4, 4):
        raise ValueError("transform must be 4x4")
    homogeneous = np.c_[points, np.ones(len(points))]
    return (homogeneous @ transform)[:, :3]
