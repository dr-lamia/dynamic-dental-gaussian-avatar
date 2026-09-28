from pathlib import Path

from src.data.public_composite import (
    ALLOWED_CLAIM_LEVEL,
    PublicComponent,
    PublicCompositeManifest,
    load_benchmark_config,
)


def test_public_benchmark_config_is_safely_labeled():
    root = Path(__file__).resolve().parents[1]
    cfg = load_benchmark_config(root / "configs" / "public_composite_benchmark.yaml")
    assert cfg["claim_level"] == ALLOWED_CLAIM_LEVEL
    assert "dental" in cfg["components"]
    assert "face_motion" in cfg["components"]
    assert "jaw_motion_engineering" in cfg["components"]


def test_composite_manifest_requires_non_patient_specific_claim(tmp_path):
    components = [
        PublicComponent(
            role="dental",
            source_name="Dental",
            source_url="https://example.org/dental",
        ),
        PublicComponent(
            role="face_motion",
            source_name="Face",
            source_url="https://example.org/face",
        ),
    ]
    manifest = PublicCompositeManifest(
        benchmark_id="test",
        claim_level=ALLOWED_CLAIM_LEVEL,
        components=components,
    )
    out = tmp_path / "manifest.json"
    manifest.save(out)
    assert out.exists()


def test_patient_specific_claim_is_rejected():
    components = [
        PublicComponent(
            role="dental",
            source_name="Dental",
            source_url="https://example.org/dental",
        ),
        PublicComponent(
            role="face_motion",
            source_name="Face",
            source_url="https://example.org/face",
        ),
    ]
    manifest = PublicCompositeManifest(
        benchmark_id="test",
        claim_level="patient_specific_digital_twin",
        components=components,
    )
    try:
        manifest.validate()
    except ValueError as exc:
        assert "claim_level" in str(exc)
    else:
        raise AssertionError("Unsafe patient-specific claim should be rejected")
