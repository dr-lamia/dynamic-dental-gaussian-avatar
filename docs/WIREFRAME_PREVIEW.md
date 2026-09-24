# Wireframe Alignment Preview

Before full Gaussian rendering is connected, the dental mesh can be projected
with a simple pinhole camera to verify gross pose/alignment.

This is a debugging aid, not a clinical visualization.

## Example

```bash
python scripts/render_alignment_preview.py \
  --obj outputs/aligned_anterior.obj \
  --alignment outputs/public_demo_alignment.json
```

The current script saves a NumPy image array. The same projection utility will
be connected to a real VHAP/Gaussian frame once its camera intrinsics/extrinsics
are available.

## Why this is useful

It allows us to debug:

- incorrect axis orientation,
- inverted Z direction,
- excessive translation,
- rotation sign errors,
- camera-centering errors,

before involving the more complex Gaussian renderer.
