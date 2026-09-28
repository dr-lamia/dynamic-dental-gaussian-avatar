# Dynamic Dental Gaussian Avatar

**A research prototype for integrating photorealistic dynamic facial avatars with patient-specific intraoral 3D geometry and mandibular motion to test 3D smile designs during movement.**

## Vision

Create a **moving 3D/4D virtual dental patient** from facial video, intraoral scans and a jaw-motion stream. The same recorded facial and mandibular motion can be replayed while switching between the original dentition and one or more proposed CAD smile designs.

## MVP input

- 30–60 s patient facial video
- upper IOS (`.stl/.ply/.obj`)
- lower IOS
- bite scan or registration information
- proposed smile-design mesh
- optional standardized jaw-motion CSV for the first static/dynamic prototypes; required for a true patient-specific mandibular-motion experiment

## MVP output

An interactive patient avatar supporting:

- rest / social smile / maximum smile
- measured or estimated mouth opening and closing
- protrusive and lateral mandibular motion when jaw tracking is available
- head rotation
- original-vs-design toggle
- multiple candidate designs on identical motion
- screenshots/video export for research comparison

## Core design principle

Do **not** model clinically relevant teeth as Gaussian appearance only.

Use a hybrid representation:

```text
Patient video
    ↓
Face tracking / FLAME parameters
    ↓
Dynamic Gaussian facial avatar
    ↓
Hybrid dental integration layer
    ├── upper IOS mesh → skull/maxillary coordinate system
    ├── lower IOS mesh → mandibular coordinate system
    ├── jaw-motion stream → per-frame mandible→face transform
    └── replaceable CAD smile-design mesh
    ↓
Motion-aware smile visualization + quantitative analytics
```

## New: patient-specific jaw-motion layer

The repository now includes `src/dental/jaw_motion.py`, which standardizes tracker outputs as per-frame rigid transforms.

Supported CSV pose encodings:

- quaternion: `tx_mm,ty_mm,tz_mm,qw,qx,qy,qz`
- Euler XYZ: `tx_mm,ty_mm,tz_mm,rx_deg,ry_deg,rz_deg`
- full homogeneous matrix: `m00 ... m33`

Optional columns include `timestamp_s` and `jaw_opening_mm`.

See [docs/PHASE1_4D_JAW_MOTION.md](docs/PHASE1_4D_JAW_MOTION.md).

## Runnable public Phase-1 demo

A fully synthetic, patient-free 4D engineering demo is included:

```bash
python scripts/run_phase1_4d_demo.py
```

It generates per-frame upper, lower and Design A OBJ meshes plus `metrics.json`, `trajectory.csv` and a summary. With the bundled example jaw trajectory, the expected engineering outputs are stored in [examples/phase1_4d_demo_expected_metrics.json](examples/phase1_4d_demo_expected_metrics.json).

See [docs/RUN_PHASE1_4D_DEMO.md](docs/RUN_PHASE1_4D_DEMO.md).

## Public online-dataset benchmark mode

If no same-patient clinical case is available, the repository can now run a **composite public-data benchmark** using separate online datasets for:

- paired dental anatomy / CBCT-IOS registration,
- dynamic face/head motion,
- jaw-motion engineering,
- clinical jaw-kinematics reference.

This mode is intentionally labeled **engineering benchmark, not patient-specific**.

Configuration:
[configs/public_composite_benchmark.yaml](configs/public_composite_benchmark.yaml)

Workflow:
[docs/PUBLIC_COMPOSITE_4D_BENCHMARK.md](docs/PUBLIC_COMPOSITE_4D_BENCHMARK.md)

Create a provenance manifest with:

```bash
python scripts/create_public_composite_manifest.py \
  --dental-path data/public_benchmark/dental/subject_001 \
  --dental-id PUBLIC_DENTAL_ID \
  --face-path data/public_benchmark/face/multiface_subject \
  --face-id PUBLIC_FACE_ID \
  --jaw-path data/public_benchmark/jaw/figshare_motion \
  --jaw-id SIMULATOR_TRAJECTORY
```

## Candidate upstream projects to benchmark

- GaussianAvatars — https://github.com/ShenhanQian/GaussianAvatars
- FlashAvatar — https://github.com/USTC3DV/FlashAvatar-code
- MeGA — https://github.com/conallwang/MeGA
- Gaussian Blendshapes — https://github.com/zjumsj/GaussianBlendshapes
- SplattingAvatar — https://github.com/initialneil/SplattingAvatar
- VHAP — https://github.com/ShenhanQian/VHAP
- MICA — https://github.com/Zielon/MICA
- DECA — https://github.com/yfeng95/DECA
- 3DTeethLand — https://github.com/nnistelrooij/3dteethland
- SlicerAutomatedDentalTools — https://github.com/DCBIA-OrthoLab/SlicerAutomatedDentalTools
- JawTrackingSystem — https://github.com/paulotto/jaw_tracking_system

> Upstream licenses differ. Do not copy/relicense upstream code until compatibility has been checked.

## Repository layout

```text
src/
  avatar/        # adapter interfaces for avatar backends
  tracking/      # FLAME/head-pose/expression tracking
  dental/        # IOS loading, jaw motion, tooth labels, dental geometry
  registration/  # face↔IOS and design↔IOS transforms
  rendering/     # hybrid face + dental renderer
  analytics/     # smile, stability and visibility metrics
configs/         # YAML configuration
scripts/         # runnable pipeline stages
docs/            # architecture, MVP, research plan
examples/        # synthetic/non-patient examples only
assets/          # safe public assets only
tests/
```

## Development phases

### Phase 1 — Avatar benchmark
Run the same short video through candidate avatar pipelines and select the best combination of quality, speed, licensing and controllability.

### Phase 2 — Dental mesh layer
Load upper/lower IOS, maintain metric scale, identify arches/teeth, and render the meshes independently of facial Gaussian splats.

### Phase 3 — Registration
Register the dental coordinate system to the facial avatar. Begin with manually assisted landmarks + rigid transformation; later automate.

### Phase 4 — Jaw-motion integration
Convert a patient jaw-motion recording into synchronized `mandible_to_face(t)` transforms and drive the lower IOS independently from the maxilla.

### Phase 5 — Replaceable smile design
Swap anterior restorative geometry without changing facial or mandibular motion.

### Phase 6 — Motion analytics
Measure tooth/lip visibility, jaw trajectory and smile-design behavior across frames.

### Phase 7 — Validation
Compare virtual measurements against reference measurements and clinician ratings on paired patient data.

## First success criterion

For one patient, reproduce a tracked smile/movement sequence and correctly display:

1. original upper dentition,
2. measured lower-arch movement,
3. proposed veneer/smile STL,
4. identical motion for original and proposed designs,
5. stable dental registration across the sequence.

That is the first publishable engineering proof of concept.

## Safety and privacy

Never commit identifiable patient video, face geometry, DICOM data, jaw-motion files containing identifiers, or unredacted clinical data to this repository. Use institutionally approved storage and access controls.
