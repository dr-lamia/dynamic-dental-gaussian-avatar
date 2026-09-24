import numpy as np
from src.registration.manual_alignment import ManualAlignment


def test_manual_alignment_translation():
    a = ManualAlignment(translation_mm=(1,2,3))
    p = np.array([[0.,0.,0.]])
    moved = a.apply(p)
    assert np.allclose(moved, [[1.,2.,3.]])


def test_manual_alignment_rotation_z_90():
    a = ManualAlignment(rotation_deg_xyz=(0,0,90))
    p = np.array([[1.,0.,0.]])
    moved = a.apply(p)
    assert np.allclose(moved, [[0.,1.,0.]], atol=1e-8)
