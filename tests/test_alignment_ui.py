from src.registration.alignment_ui import clamp, DEFAULT_LIMITS


def test_clamp():
    assert clamp(200, -100, 100) == 100
    assert clamp(-200, -100, 100) == -100
    assert clamp(5, -100, 100) == 5


def test_default_limits():
    assert DEFAULT_LIMITS.translation_step_mm > 0
    assert DEFAULT_LIMITS.rotation_step_deg > 0
