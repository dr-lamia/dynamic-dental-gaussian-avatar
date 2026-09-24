"""Frame-level smile-analysis placeholders.

Future metrics: incisor display, gingival display, midline, smile arc,
buccal corridor, tooth visibility and lip trajectories.
"""


def tooth_visibility_fraction(visible_frames: int, total_frames: int) -> float:
    if total_frames <= 0:
        raise ValueError("total_frames must be > 0")
    return visible_frames / total_frames
