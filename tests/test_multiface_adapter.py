from pathlib import Path
import numpy as np

from src.tracking.multiface import (
    discover_expression,
    load_headpose_matrix,
)


def test_discover_expression_pairs_obj_and_transform(tmp_path):
    root = tmp_path / "m--demo--GHS"
    expr = root / "tracked_mesh" / "E009_Smile_Mouth_Open"
    expr.mkdir(parents=True)

    (expr / "000001.obj").write_text("v 0 0 0\n", encoding="utf-8")
    (expr / "000001_transform.txt").write_text(
        "1 0 0 0\n0 1 0 0\n0 0 1 0\n0 0 0 1\n",
        encoding="utf-8",
    )

    seq = discover_expression(root, "E009_Smile_Mouth_Open")
    assert len(seq.frames) == 1
    assert seq.frames[0].frame_id == "000001"


def test_headpose_matrix_parser(tmp_path):
    path = tmp_path / "000001_transform.txt"
    path.write_text(
        "1 0 0 1\n0 1 0 2\n0 0 1 3\n0 0 0 1\n",
        encoding="utf-8",
    )
    M = load_headpose_matrix(path)
    assert M.shape == (4, 4)
    assert np.allclose(M[:3, 3], [1, 2, 3])


def test_headpose_parser_accepts_brackets_and_commas(tmp_path):
    path = tmp_path / "bracket_transform.txt"
    path.write_text(
        "[[1, 0, 0, 1],\n"
        " [0, 1, 0, 2],\n"
        " [0, 0, 1, 3],\n"
        " [0, 0, 0, 1]]\n",
        encoding="utf-8",
    )
    M = load_headpose_matrix(path)
    assert np.allclose(M[:3, 3], [1, 2, 3])


def test_headpose_parser_promotes_3x4(tmp_path):
    path = tmp_path / "three_by_four_transform.txt"
    path.write_text(
        "1,0,0,1\n0,1,0,2\n0,0,1,3\n",
        encoding="utf-8",
    )
    M = load_headpose_matrix(path)
    assert M.shape == (4, 4)
    assert np.allclose(M[3], [0, 0, 0, 1])
    assert np.allclose(M[:3, 3], [1, 2, 3])
