import numpy as np
from src.tracking.vhap_flame_regions import mouth_polygon_from_rings, aperture_height_px


def test_mouth_polygon_closes_from_two_rings():
    upper = np.array([[0, 1], [1, 0], [2, 1]], float)
    lower = np.array([[0, 3], [1, 4], [2, 3]], float)
    poly = mouth_polygon_from_rings(upper, lower)
    assert poly.shape == (6, 2)
    assert np.allclose(poly[:3], upper)
    assert np.allclose(poly[3:], lower[::-1])


def test_aperture_height():
    upper = np.array([[0, 1], [1, 1], [2, 1]], float)
    lower = np.array([[0, 4], [1, 5], [2, 4]], float)
    assert aperture_height_px(upper, lower) == 3.0
