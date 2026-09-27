from pathlib import Path
import shutil

from src.dental.case_manifest import CaseManifest
from scripts.validate_case_inputs import validate_case


def test_complete_patient_case_validates_ready(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    case_dir = tmp_path / "P001"
    case_dir.mkdir()

    for name in ["facial_video.mp4", "upper_ios.stl", "lower_ios.stl", "bite.stl", "design_A.stl"]:
        (case_dir / name).write_bytes(b"synthetic-test-placeholder")

    shutil.copy(
        repo_root / "examples" / "jaw_motion.example.csv",
        case_dir / "jaw_motion.csv",
    )

    manifest = CaseManifest(
        case_id="P001",
        video="facial_video.mp4",
        upper_mesh="upper_ios.stl",
        lower_mesh="lower_ios.stl",
        design_meshes=["design_A.stl"],
        bite_mesh="bite.stl",
        jaw_motion_csv="jaw_motion.csv",
    )
    manifest_path = case_dir / "case.json"
    manifest.save(manifest_path)

    report = validate_case(manifest_path)
    assert report["ready"] is True
    assert report["missing"] == []
    assert report["jaw_motion"]["frames"] == 6
    assert report["jaw_motion"]["max_jaw_opening_mm"] == 8.0


def test_incomplete_patient_case_reports_missing_files(tmp_path):
    case_dir = tmp_path / "P002"
    case_dir.mkdir()

    manifest = CaseManifest(
        case_id="P002",
        video="missing_video.mp4",
        upper_mesh="missing_upper.stl",
        lower_mesh="missing_lower.stl",
        design_meshes=["missing_design.stl"],
    )
    manifest_path = case_dir / "case.json"
    manifest.save(manifest_path)

    report = validate_case(manifest_path)
    assert report["ready"] is False
    assert set(report["missing"]) == {
        "video",
        "upper_mesh",
        "lower_mesh",
        "design_mesh_1",
    }
