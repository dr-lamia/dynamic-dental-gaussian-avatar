from src.registration.transforms import DentalTransforms


def test_identity_transforms():
    t = DentalTransforms.identity()
    assert t.face_to_world.shape == (4, 4)
    assert t.upper_to_face.shape == (4, 4)
