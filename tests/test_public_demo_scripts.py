from pathlib import Path


def test_public_demo_scripts_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "scripts" / "public_vhap_demo.sh").exists()
    assert (root / "scripts" / "public_gaussian_avatar_demo.sh").exists()


def test_public_demo_uses_public_sequence():
    root = Path(__file__).resolve().parents[1]
    txt = (root / "scripts" / "public_vhap_demo.sh").read_text()
    assert "obama.mp4" in txt
    assert "patient_data" not in txt
