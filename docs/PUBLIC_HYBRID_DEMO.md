# End-to-End Public Hybrid Demo

## Goal

Combine:

1. a public VHAP monocular face video,
2. VHAP FLAME tracking,
3. GaussianAvatars,
4. one public Teeth3DS upper scan,
5. our registration + occlusion + temporal-stability modules.

No private patient data are required.

## Inputs

- Public VHAP example video (the upstream monocular documentation uses
  `obama.mp4`)
- One locally downloaded Teeth3DS upper OBJ
- Its paired JSON label file
- Local clones of VHAP and GaussianAvatars
- Licensed FLAME assets

## Step 1 — select public dental case

```bash
python scripts/find_teeth3ds_case.py --root /secure/datasets/teeth3ds
```

## Step 2 — create a complete execution plan

```bash
python scripts/run_public_hybrid_demo.py \
  --vhap-repo /path/to/VHAP \
  --gaussian-repo /path/to/GaussianAvatars \
  --public-video /path/to/VHAP/data/monocular/obama.mp4 \
  --teeth-obj /secure/.../<case>_upper.obj \
  --teeth-json /secure/.../<case>_upper.json \
  --execute-dental
```

This creates:

- selected anterior Teeth3DS OBJ
- execution plan JSON
- expected VHAP export path
- expected GaussianAvatars model path
- required hybrid registration/occlusion/validation steps

## Step 3 — GPU face pipeline

Run the already supplied:

- `scripts/public_vhap_demo.sh`
- `scripts/public_gaussian_avatar_demo.sh`

inside their respective environments.

## Step 4 — hybrid integration

Once tracked FLAME frames are available:

- obtain ordered upper/lower lip-ring vertices from VHAP
- project them into camera coordinates
- create the dynamic mouth aperture
- estimate `T_upper_to_face`
- place the Teeth3DS mesh
- depth-test teeth against facial depth
- render original/design states
- calculate temporal drift

## Primary technical outcomes

The public proof-of-concept will report:

- landmark registration RMSE (mm)
- mean/max/P95 temporal drift (mm)
- lip aperture behavior over time
- avatar reconstruction/tracking timings
- render FPS
- qualitative lip–teeth occlusion errors

## Limitation

The face and Teeth3DS scan come from different people in this fully public
engineering demo. Therefore this experiment validates the **software pipeline**,
not anatomical patient-specific accuracy. Patient-specific scientific
validation requires paired facial video and IOS from the same participant.
