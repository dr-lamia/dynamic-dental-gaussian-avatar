# Dynamic Dental Gaussian Avatar

**A research prototype for integrating photorealistic dynamic facial avatars with patient-specific intraoral 3D geometry to test 3D smile designs during facial movement.**

## Vision

Create a **moving 3D/4D virtual dental patient** from facial video and intraoral scans. The same recorded facial motion can be replayed while switching between the original dentition and one or more proposed CAD smile designs.

## MVP input

- 30–60 s patient facial video
- upper IOS (`.stl/.ply/.obj`)
- lower IOS
- bite scan or registration information
- proposed smile-design mesh

## MVP output

An interactive patient avatar supporting:

- rest / social smile / maximum smile
- mouth opening and closing
- head rotation
- original-vs-design toggle
- multiple candidate designs on identical facial motion
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
    ├── lower IOS mesh → mandibular transform
    └── replaceable CAD smile-design mesh
    ↓
Motion-aware smile visualization + quantitative analytics
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

> Upstream licenses differ. Do not copy/relicense upstream code until compatibility has been checked. GaussianAvatars, for example, has non-commercial restrictions in its published repository license.

## Repository layout

```text
src/
  avatar/        # adapter interfaces for avatar backends
  tracking/      # FLAME/head-pose/expression tracking
  dental/        # IOS loading, tooth labels, dental geometry
  registration/  # face↔IOS and design↔IOS transforms
  rendering/     # hybrid face + dental renderer
  analytics/     # smile and visibility metrics
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

### Phase 4 — Replaceable smile design
Swap anterior restorative geometry without changing facial motion.

### Phase 5 — Motion analytics
Measure tooth/lip visibility and smile-design behavior across frames.

### Phase 6 — Validation
Compare virtual measurements against reference measurements and clinician ratings on paired patient data.

## First success criterion

For one patient, reproduce a tracked smile sequence and correctly display:

1. original upper dentition,
2. proposed veneer/smile STL,
3. identical facial movement for both,
4. stable dental registration across the sequence.

That is the first publishable engineering proof of concept.

## Safety and privacy

Never commit identifiable patient video, face geometry, DICOM data or unredacted clinical data to this repository. Use institutionally approved storage and access controls.
