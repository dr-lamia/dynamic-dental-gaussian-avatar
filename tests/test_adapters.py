from src.avatar.external import GaussianAvatarsAdapter, FlashAvatarAdapter
from src.tracking.vhap import VHAPAdapter, VHAPPaths
from pathlib import Path


def test_gaussian_avatar_commands():
    a = GaussianAvatarsAdapter("/tmp/GaussianAvatars")
    cmd = a.train_command("/tmp/export", "/tmp/model")
    assert cmd[:2] == ("python", "train.py")
    assert "--bind_to_mesh" in cmd


def test_flashavatar_command():
    a = FlashAvatarAdapter("/tmp/FlashAvatar")
    assert a.train_command("patient_001") == ("python", "train.py", "--idname", "patient_001")


def test_vhap_pipeline_commands():
    a = VHAPAdapter("/tmp/VHAP")
    p = VHAPPaths(
        video=Path("/secure/patient.mp4"),
        data_root=Path("/secure/data"),
        sequence="patient",
        tracking_output=Path("/secure/output"),
        export_output=Path("/secure/export"),
    )
    assert "robust_video_matting" in a.preprocess_command(p.video)
    assert "vhap/track.py" in a.track_command(p)
    assert "vhap/export_as_nerf_dataset.py" in a.export_command(p)
