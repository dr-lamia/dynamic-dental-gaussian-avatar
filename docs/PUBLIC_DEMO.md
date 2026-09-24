# Public VHAP → GaussianAvatars Demo

This is the first reproducible integration test for the Dynamic Dental Gaussian Avatar project.

## Why a public example first?

It isolates engineering problems from patient-specific data and privacy concerns. The purpose is to validate video preprocessing, facial landmark detection, FLAME tracking, NeRF/3DGS export, Gaussian-avatar training, motion rendering, and access to stable face/jaw parameters for the future dental layer.

## Public source

The upstream VHAP documentation demonstrates its monocular workflow with `obama.mp4` and links a public monocular-video source in its README.

- VHAP: https://github.com/ShenhanQian/VHAP
- GaussianAvatars: https://github.com/ShenhanQian/GaussianAvatars

Do not redistribute the public example here. Download it from the upstream source and obey its terms.

## Step A — VHAP

Install VHAP according to its official instructions, obtain FLAME 2023 assets from the official FLAME source, and place the public video at:

```
VHAP/data/monocular/obama.mp4
```

Then, from the VHAP repository:

```bash
/path/to/dynamic-dental-gaussian-avatar/scripts/public_vhap_demo.sh obama.mp4
```

Expected export:

```
VHAP/export/monocular/obama_whiteBg_staticOffset_maskBelowLine/
```

## Step B — GaussianAvatars

Activate the separate GaussianAvatars environment and run:

```bash
/path/to/dynamic-dental-gaussian-avatar/scripts/public_gaussian_avatar_demo.sh \
  /path/to/VHAP/export/monocular/obama_whiteBg_staticOffset_maskBelowLine
```

This trains a FLAME-bound Gaussian avatar and renders the tracked motion.

## Record these outputs

- video resolution, duration, frame count
- GPU and peak VRAM
- preprocessing time
- tracking time
- Gaussian training time
- render FPS
- tracking drift/failures
- jaw/mouth alignment
- lip and dental-region artifacts

## Important limitation

A GaussianAvatars issue documents a case where monocular VHAP driving parameters produced less natural reenactment than multiview tracking. This first run is therefore a pipeline-validation experiment; motion quality will be benchmarked rather than assumed.

## Success criterion

- VHAP produces tracked FLAME parameters.
- The export loads into GaussianAvatars.
- A moving avatar is rendered.
- Jaw/expression trajectories are available for the dental-registration module.

## Next step

Extract representative rest, early-smile, maximum-smile and mouth-open frames and use them to design the first upper-IOS alignment experiment.
