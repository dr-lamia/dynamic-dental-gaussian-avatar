"""Adapters for external avatar repositories.

No upstream source code is vendored here. These adapters build commands that are
run inside the upstream project's own environment.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Sequence


@dataclass(frozen=True)
class CommandResult:
    args: tuple[str, ...]
    returncode: int


def _run(args: Sequence[str], cwd: str | Path, execute: bool = True) -> CommandResult:
    cmd = tuple(str(x) for x in args)
    if not execute:
        return CommandResult(cmd, 0)
    proc = subprocess.run(cmd, cwd=Path(cwd), check=False)
    return CommandResult(cmd, proc.returncode)


class GaussianAvatarsAdapter:
    def __init__(self, repo_dir: str | Path):
        self.repo_dir = Path(repo_dir)

    def train_command(
        self,
        source_path: str | Path,
        model_path: str | Path,
        port: int = 60000,
    ) -> tuple[str, ...]:
        return (
            "python", "train.py",
            "-s", str(source_path),
            "-m", str(model_path),
            "--eval",
            "--bind_to_mesh",
            "--white_background",
            "--port", str(port),
        )

    def render_command(
        self,
        model_path: str | Path,
        target_motion_path: str | Path | None = None,
        camera_id: int | None = None,
    ) -> tuple[str, ...]:
        cmd = ["python", "render.py", "-m", str(model_path)]
        if target_motion_path is not None:
            cmd += ["-t", str(target_motion_path)]
        if camera_id is not None:
            cmd += ["--select_camera_id", str(camera_id)]
        return tuple(cmd)

    def run_train(self, *args, execute: bool = True, **kwargs) -> CommandResult:
        return _run(self.train_command(*args, **kwargs), self.repo_dir, execute)


class FlashAvatarAdapter:
    def __init__(self, repo_dir: str | Path):
        self.repo_dir = Path(repo_dir)

    def train_command(self, identity: str) -> tuple[str, ...]:
        return ("python", "train.py", "--idname", identity)

    def test_command(self, identity: str, checkpoint: str | Path) -> tuple[str, ...]:
        return (
            "python", "test.py",
            "--idname", identity,
            "--checkpoint", str(checkpoint),
        )

    def run_train(self, identity: str, execute: bool = True) -> CommandResult:
        return _run(self.train_command(identity), self.repo_dir, execute)
