"""VHAP monocular-video adapter.

VHAP is kept as an external dependency because its license and environment are
independent of this repository.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass
class VHAPPaths:
    video: Path
    data_root: Path
    sequence: str
    tracking_output: Path
    export_output: Path


class VHAPAdapter:
    def __init__(self, repo_dir: str | Path):
        self.repo_dir = Path(repo_dir)

    def preprocess_command(self, video: str | Path) -> tuple[str, ...]:
        return (
            "python", "vhap/preprocess_video.py",
            "--input", str(video),
            "--matting_method", "robust_video_matting",
        )

    def track_command(self, p: VHAPPaths) -> tuple[str, ...]:
        return (
            "python", "vhap/track.py",
            "--data.root_folder", str(p.data_root),
            "--exp.output_folder", str(p.tracking_output),
            "--data.sequence", p.sequence,
        )

    def export_command(self, p: VHAPPaths) -> tuple[str, ...]:
        return (
            "python", "vhap/export_as_nerf_dataset.py",
            "--src_folder", str(p.tracking_output),
            "--tgt_folder", str(p.export_output),
            "--background-color", "white",
        )

    def run(self, command: tuple[str, ...], execute: bool = True) -> int:
        if not execute:
            return 0
        return subprocess.run(command, cwd=self.repo_dir, check=False).returncode
