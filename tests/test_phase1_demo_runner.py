import json
from pathlib import Path
import numpy as np

from scripts.run_phase1_4d_demo import run_demo


def test_phase1_demo_runs_end_to_end(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    jaw_csv = repo_root / "examples" / "jaw_motion.example.csv"

    metrics = run_demo(jaw_csv, tmp_path)

    assert metrics["frames"] == 6
    assert np.isclose(metrics["duration_s"], 0.083)
    assert np.isclose(metrics["path_length_mm"], 8.158431221748456)
    assert np.isclose(metrics["max_displacement_from_start_mm"], 4.079215610874228)
    assert np.isclose(metrics["max_rotation_from_start_deg"], 3.0003415532283375)
    assert metrics["max_jaw_opening_mm"] == 8.0
    assert metrics["synthetic_demo"] is True

    obj_files = sorted((tmp_path / "frames").glob("*.obj"))
    assert len(obj_files) == 18

    assert (tmp_path / "trajectory.csv").exists()
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "SUMMARY.md").exists()

    saved = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))
    assert saved["frames"] == 6
