"""Create reproducible backend command plans and benchmark records.

This does not install or vendor upstream projects. It helps run the same patient
case through isolated external environments.
"""
from argparse import ArgumentParser
import json
from pathlib import Path

from src.avatar.external import GaussianAvatarsAdapter, FlashAvatarAdapter


def main() -> None:
    p = ArgumentParser()
    p.add_argument("--gaussian-avatars")
    p.add_argument("--flashavatar")
    p.add_argument("--source")
    p.add_argument("--model-out", default="outputs/gaussian_avatar")
    p.add_argument("--identity", default="patient_001")
    p.add_argument("--out", default="outputs/backend_plan.json")
    a = p.parse_args()

    plan = {}
    if a.gaussian_avatars and a.source:
        ga = GaussianAvatarsAdapter(a.gaussian_avatars)
        plan["gaussian_avatars"] = {
            "train": ga.train_command(a.source, a.model_out),
            "render": ga.render_command(a.model_out),
        }

    if a.flashavatar:
        fa = FlashAvatarAdapter(a.flashavatar)
        plan["flashavatar"] = {
            "train": fa.train_command(a.identity),
        }

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
