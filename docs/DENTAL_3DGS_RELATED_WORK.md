# Dental 3DGS Related Work

A useful public repository identified during development is:

- **lgarbayo/dental-3dgs-lab**
  https://github.com/lgarbayo/dental-3dgs-lab

It demonstrates a mesh → synthetic calibrated views → 3D Gaussian Splatting
workflow for dental scans, including:

- OBJ + FDI labels
- synthetic camera views with exact known poses
- `transforms.json`
- 3DGS training with `gsplat`
- held-out view evaluation
- orbit rendering

## Why it matters for this project

Our project does **not** need to convert the real dental IOS into Gaussians for
the first MVP; keeping dental geometry as a true mesh is preferable for metric
restorative work.

However, the repository is valuable for two later experiments:

1. **Dental appearance layer**
   - keep the metric IOS mesh as geometric truth,
   - optionally learn a Gaussian appearance representation for realistic
     enamel/gingival rendering.

2. **Controlled renderer validation**
   - render synthetic calibrated views from a known dental mesh,
   - use those exact cameras to test our dental projection/compositor.

## Important licensing note

At the time inspected, no repository-level LICENSE file was found in
`lgarbayo/dental-3dgs-lab`. Therefore we should treat its source code as
**reference-only unless explicit permission/license is confirmed**.

Also, its README describes a Teeth3DS-derived download differently from the
official Teeth3DS repository. For dataset terms we follow the **official
3DTeethSeg/Teeth3DS source**, which currently states CC BY-NC-ND 4.0 for the
dataset and 1,800 scans from 900 patients.

Official dataset source:
https://github.com/abenhamadou/3DTeethSeg_MICCAI_Challenges
