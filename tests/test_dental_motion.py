import numpy as np
from src.rendering.frame_state import FrameState
from src.dental.motion import upper_vertices_for_frame, lower_vertices_for_frame


def test_upper_follows_head_translation():
    v = np.array([[1.0, 2.0, 3.0]])
    I = np.eye(4)
    face = np.eye(4)
    face[:3, 3] = [10.0, 0.0, 0.0]
    frame = FrameState(0, face, I)
    moved = upper_vertices_for_frame(v, I, frame)
    assert np.allclose(moved, [[11.0, 2.0, 3.0]])


def test_lower_has_independent_mandible_motion():
    v = np.array([[0.0, 0.0, 0.0]])
    I = np.eye(4)
    jaw = np.eye(4)
    jaw[:3, 3] = [0.0, -5.0, 0.0]
    frame = FrameState(0, I, jaw)
    moved = lower_vertices_for_frame(v, I, frame)
    assert np.allclose(moved, [[0.0, -5.0, 0.0]])
