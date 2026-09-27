import tempfile
from pathlib import Path
import numpy as np

from src.dental.jaw_motion import (
    JawMotionSample,
    JawMotionSequence,
    load_jaw_motion_csv,
    save_jaw_motion_csv,
)


def _write(text: str) -> Path:
    handle = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
    handle.write(text)
    handle.close()
    return Path(handle.name)


def test_load_quaternion_translation_and_frame_state():
    path = _write(
        "frame_index,timestamp_s,tx_mm,ty_mm,tz_mm,qw,qx,qy,qz,jaw_opening_mm\n"
        "0,0.0,1,2,3,1,0,0,0,4.5\n"
    )
    seq = load_jaw_motion_csv(path)
    sample = seq.samples[0]
    assert np.allclose(sample.mandible_to_face[:3, 3], [1, 2, 3])
    assert np.allclose(sample.mandible_to_face[:3, :3], np.eye(3))
    frame = seq.to_frame_state(0)
    assert frame.jaw_opening == 4.5


def test_load_euler_z_rotation():
    path = _write(
        "frame_index,tx_mm,ty_mm,tz_mm,rx_deg,ry_deg,rz_deg\n"
        "0,0,0,0,0,0,90\n"
    )
    seq = load_jaw_motion_csv(path)
    rotation = seq.samples[0].mandible_to_face[:3, :3]
    moved = rotation @ np.array([1.0, 0.0, 0.0])
    assert np.allclose(moved, [0.0, 1.0, 0.0], atol=1e-7)


def test_round_trip_matrix_csv():
    transform = np.eye(4)
    transform[:3, 3] = [2.0, -3.0, 4.0]
    seq = JawMotionSequence([JawMotionSample(0, transform, timestamp_s=0.25)])

    handle = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    handle.close()
    path = Path(handle.name)
    save_jaw_motion_csv(seq, path)
    loaded = load_jaw_motion_csv(path)
    assert np.allclose(loaded.samples[0].mandible_to_face, transform)
    assert loaded.samples[0].timestamp_s == 0.25


def test_rejects_non_increasing_frames():
    identity = np.eye(4)
    try:
        JawMotionSequence([
            JawMotionSample(1, identity),
            JawMotionSample(1, identity),
        ])
    except ValueError as exc:
        assert "strictly increasing" in str(exc)
    else:
        raise AssertionError("Expected duplicate frame indices to fail")
