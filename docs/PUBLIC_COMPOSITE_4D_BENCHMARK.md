# Public Composite 4D Dental Benchmark

## Purpose

This workflow lets the project develop and test a 4D dental pipeline using **online public datasets only**.

It deliberately combines separate public sources for separate modules:

- dental anatomy / CBCT-IOS registration
- dynamic face/head motion
- jaw-motion engineering
- clinical jaw-kinematics reference

Because these components do not belong to one person, the result is a **composite engineering benchmark**, not a patient-specific digital twin.

## Selected online datasets

### Dental anatomy

**3D multimodal dental dataset based on CBCT and oral scan**

- 289 paired subjects after screening/desensitization
- paired CBCT + oral scan
- CC BY 4.0
- source:
  https://figshare.com/articles/dataset/_b_3D_multimodal_dental_dataset_based_on_CBCT_and_oral_scan_b_/26965903

Use one paired subject at a time. Do not split the CBCT from one public subject and the oral scan from another.

### Dynamic face/head motion

**MultiFace**

- 13 identities
- multiview facial video
- tracked meshes
- head pose
- audio
- partial/subset downloading supported by the official repository

Source:
https://github.com/facebookresearch/multiface

For storage-limited development, download one identity and only the tracked-mesh/head-pose assets needed for the benchmark rather than the full dataset.

### Jaw-motion engineering

**Accelerometry-enhanced Magnetic Sensor for Intra-oral Continuous Jaw Motion Tracking and Bruxism Detection**

- Figshare dataset
- CC BY 4.0
- small engineering dataset
- useful for trajectory-processing experiments
- includes simulator/controlled jaw trajectories; do not label these as patient-specific clinical motion

Source:
https://figshare.com/articles/dataset/Accelerometry-enhanced_Magnetic_Sensor_for_Intra-oral_Continuous_Jaw_Motion_Tracking_and_Bruxism_Detection/13397528

### Clinical jaw-kinematics reference

**Premolar extraction in orthodontics and its effect on mandibular kinematics**

- 90 subjects
- 45 extraction-treated patients + 45 paired untreated controls
- CADIAX-derived 3D kinematic variables
- CC BY 4.0

Source:
https://data.mendeley.com/datasets/3tcs5c47jg

Use this as an external clinical reference for plausible kinematic ranges and group-level comparisons. It is not a synchronized frame-by-frame motion stream for the dental or facial subjects.

## Benchmark assembly

The composite benchmark is:

```text
Public dental subject
    ├── oral scan / dental geometry
    └── paired CBCT
             +
Public face identity
    ├── tracked facial mesh
    └── head pose over time
             +
Public jaw engineering trajectory
    └── standardized mandible transform sequence
             ↓
COMPOSITE PUBLIC 4D BENCHMARK
             ↓
registration / rendering / motion / analytics testing
```

## What we can claim

Appropriate language:

> A composite public-data benchmark was constructed to test the technical integration of dental geometry, facial dynamics, and mandibular-motion modules.

Do **not** write:

> A patient-specific 4D dental digital twin was constructed.

The latter requires synchronized modalities from the same subject.

## Local folder suggestion

```text
data/public_benchmark/
├── dental/
│   └── subject_001/
├── face/
│   └── multiface_subject/
├── jaw/
│   └── figshare_motion/
└── public_composite_manifest.json
```

## Create the provenance manifest

```bash
python scripts/create_public_composite_manifest.py \
  --dental-path data/public_benchmark/dental/subject_001 \
  --dental-id PUBLIC_DENTAL_ID \
  --face-path data/public_benchmark/face/multiface_subject \
  --face-id PUBLIC_FACE_ID \
  --jaw-path data/public_benchmark/jaw/figshare_motion \
  --jaw-id SIMULATOR_TRAJECTORY \
  --out data/public_benchmark/public_composite_manifest.json
```

The generated manifest records source URLs and component IDs so figures, tables, and later manuscripts retain provenance.

## Recommended experiment sequence

1. **Dental module**
   - choose 1–5 paired dental subjects
   - verify oral-scan scale
   - perform CBCT-IOS registration
   - report registration error

2. **Face-motion module**
   - choose one MultiFace identity/expression subset
   - ingest tracked meshes/head poses
   - validate frame ordering and temporal stability

3. **Jaw-motion module**
   - ingest the Figshare motion data
   - convert it to the repository's standardized per-frame transform representation
   - report path length, displacement, rotation, and continuity

4. **Composite render**
   - place the dental component into the facial coordinate system using a clearly labeled engineering registration
   - drive the lower arch with the jaw-motion transform
   - render the sequence

5. **Robustness experiment**
   - repeat with multiple dental subjects and motion trajectories
   - report module-level failure rates and sensitivity to registration perturbation

## Best first paper using only public data

A defensible paper direction is:

**Open Public-Data Benchmark for Modular 4D Dental Virtual Patient Reconstruction: Integration of Dental Geometry, Facial Dynamics, and Mandibular Motion**

This would be a technical methods/benchmark paper. A later same-patient clinical study can validate the full digital-twin claim.
