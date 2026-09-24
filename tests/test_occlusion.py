import numpy as np
from src.rendering.occlusion import compose_dental_visibility
from src.tracking.mouth_region import polygon_mask


def test_dental_visible_only_inside_mouth():
    dental = np.full((5, 5), 5.0)
    face = np.full((5, 5), 10.0)
    mouth = np.zeros((5, 5), dtype=bool)
    mouth[2, 2] = True

    vis = compose_dental_visibility(dental, face, mouth)
    assert vis.sum() == 1
    assert vis[2, 2]


def test_dental_hidden_when_behind_face():
    dental = np.full((3, 3), 10.0)
    face = np.full((3, 3), 5.0)
    mouth = np.ones((3, 3), dtype=bool)
    vis = compose_dental_visibility(dental, face, mouth)
    assert not vis.any()


def test_polygon_mask_rasterizes():
    poly = np.array([[1, 1], [3, 1], [3, 3], [1, 3]], dtype=float)
    mask = polygon_mask(5, 5, poly)
    assert mask[2, 2]
    assert not mask[0, 0]
