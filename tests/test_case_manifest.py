import json
from pathlib import Path

from src.dental.case_manifest import CaseManifest


def test_manifest_round_trip_and_relative_resolution(tmp_path):
    case_dir = tmp_path / "P001"
    case_dir.mkdir()

    manifest = CaseManifest(
        case_id="P001",
        video="facial_video.mp4",
        upper_mesh="upper.stl",
        lower_mesh="lower.stl",
        design_meshes=["design_A.stl"],
        bite_mesh="bite.stl",
        jaw_motion_csv="jaw_motion.csv",
    )
    path = case_dir / "case.json"
    manifest.save(path)

    loaded = CaseManifest.load(path)
    assert loaded.case_id == "P001"
    assert loaded.design_meshes == ["design_A.stl"]

    resolved = loaded.resolve_files(path)
    assert resolved["video"] == (case_dir / "facial_video.mp4").resolve()
    assert resolved["jaw_motion_csv"] == (case_dir / "jaw_motion.csv").resolve()


def test_manifest_requires_design_mesh():
    manifest = CaseManifest(
        case_id="P001",
        video="video.mp4",
        upper_mesh="upper.stl",
        lower_mesh="lower.stl",
        design_meshes=[],
    )
    try:
        manifest.validate_extensions()
    except ValueError as exc:
        assert "At least one design mesh" in str(exc)
    else:
        raise AssertionError("Expected empty design list to fail")
