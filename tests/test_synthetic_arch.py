import numpy as np
from src.dental.synthetic_arch import build_maxillary_arch, default_maxillary_specs
from src.registration.landmarks import maxillary_anchor_template
from src.registration.rigid import estimate_rigid_transform, apply_transform
from src.analytics.registration_metrics import summarize_errors_mm


def test_synthetic_arch_has_14_teeth():
    specs = default_maxillary_specs()
    assert len(specs) == 14
    assert specs[0].fdi == 17
    assert specs[-1].fdi == 27


def test_registration_pipeline_recovers_known_pose():
    anchors = maxillary_anchor_template()
    names = list(anchors)
    source = np.vstack([anchors[n] for n in names])

    T_true = np.eye(4)
    T_true[:3, 3] = [12.0, -4.0, 80.0]
    target = apply_transform(source, T_true)

    T_est = estimate_rigid_transform(source, target)
    predicted = apply_transform(source, T_est)
    m = summarize_errors_mm(predicted, target)
    assert m["rmse_mm"] < 1e-8


def test_mesh_builds():
    vertices, faces, labels = build_maxillary_arch()
    assert vertices.shape[1] == 3
    assert faces.shape[1] == 3
    assert len(vertices) == len(labels)
    assert len(set(labels.tolist())) == 14
