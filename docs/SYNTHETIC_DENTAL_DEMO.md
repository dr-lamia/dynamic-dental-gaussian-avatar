# Synthetic Dental Overlay Demo

## Purpose

This demo creates a reproducible, non-patient maxillary mesh so the dental
integration layer can be developed before we have a completed Gaussian avatar
or a restricted public IOS dataset locally.

The mesh is **schematic and not anatomically valid for clinical use**.

## Generate the mesh

From the project repository:

```bash
python scripts/generate_synthetic_arch.py
```

Default output:

```
outputs/synthetic_maxillary_arch.obj
```

The mesh contains 14 schematic upper teeth corresponding to FDI 17–27
(excluding third molars).

## First registration experiment

1. Generate the synthetic arch.
2. Use five reference anchors:
   - incisal midline
   - left/right canine
   - left/right first molar
3. Create a known rigid transform.
4. Estimate the transform from corresponding landmarks.
5. Measure landmark RMSE.
6. Project transformed dental points using the same virtual camera as the
   avatar frame.
7. Confirm that a second dental design can be swapped without changing the
   avatar/camera transforms.

## Why this exists

It separates four engineering questions:

- Can our registration math recover the dental pose?
- Can we preserve metric scale?
- Can we project dental geometry into the avatar camera?
- Can we swap designs while preserving the same motion?

Once those pass, replace the synthetic arch with a real IOS mesh.

## Public realistic replacement

Teeth3DS / 3DTeethSeg provides public upper/lower intraoral OBJ meshes with FDI
tooth labels. Because access/license terms apply, we reference the dataset
externally instead of redistributing its meshes in this repository.

Source:
https://github.com/abenhamadou/3DTeethSeg_MICCAI_Challenges
