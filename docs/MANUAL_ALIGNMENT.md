# Manual Alignment for the Cross-Subject Public Demo

The public VHAP face and the public Teeth3DS scan come from different people.
Therefore there is no anatomically correct registration between them.

For the **engineering demo only**, we allow a manual rigid transform to place the
dental mesh visually inside the mouth. The transform is always saved as a JSON
file containing:

- translation in millimeters,
- XYZ rotation in degrees,
- the resulting 4×4 homogeneous matrix,
- a warning that the alignment is not anatomical validation.

## Create an alignment

Example:

```bash
python scripts/create_alignment.py \
  --tx 0 --ty -12 --tz 70 \
  --rx 5 --ry 0 --rz 0 \
  --out outputs/public_demo_alignment.json
```

## Apply it to Teeth3DS anterior teeth

```bash
python scripts/apply_alignment_to_teeth3ds.py \
  --obj /secure/.../<case>_upper.obj \
  --json /secure/.../<case>_upper.json \
  --alignment outputs/public_demo_alignment.json \
  --out outputs/aligned_anterior.obj
```

## Why save the transform?

Every public-demo render must be reproducible. A visual alignment should never
exist only as an undocumented mouse movement in a viewer.

The saved alignment lets us:

- regenerate the same frames,
- compare Design A/B/C under identical geometry,
- record exactly what transform was used,
- later replace the manual transform with true patient-specific registration.

## What this does *not* prove

A visually acceptable cross-subject placement cannot be interpreted as:

- registration accuracy,
- anatomical correspondence,
- clinical fit,
- patient-specific smile-design validity.

Those claims require paired facial and intraoral data from the same participant.
