# Run the Phase-1 4D Dental Demo

This demo proves the jaw-motion integration without any patient data.

## What it does

It creates schematic upper and lower arches, reads the standardized jaw-motion CSV, drives the lower arch independently frame by frame, applies the same maxillary/head motion to the original upper arch and a synthetic Design A, and exports quantitative motion measurements.

## Run

From the repository root:

```bash
python scripts/run_phase1_4d_demo.py
```

Optional paths:

```bash
python scripts/run_phase1_4d_demo.py \
  --jaw-motion examples/jaw_motion.example.csv \
  --out outputs/phase1_4d_demo
```

## Output

```text
outputs/phase1_4d_demo/
├── frames/
│   ├── frame_0000_upper.obj
│   ├── frame_0000_lower.obj
│   ├── frame_0000_design_a.obj
│   └── ...
├── metrics.json
├── trajectory.csv
└── SUMMARY.md
```

### metrics.json

Contains:

- number of frames
- duration
- translational jaw path length
- maximum displacement from the start
- maximum rotation from the start
- maximum supplied jaw opening

### trajectory.csv

Contains frame-level:

- jaw translation
- displacement from start
- rotation from start
- supplied jaw opening
- transformed lower-arch centroid

## What this demo proves

The maxillary arch and Design A share one stable maxillary/head transform, while the lower arch receives an additional time-varying `mandible_to_face(t)` transform.

That is the essential geometry needed for the project's 4D mandibular component.

## What it does NOT prove

The included arches and motion are synthetic. They do not establish clinical accuracy. Clinical validation requires a same-patient capture containing real upper/lower IOS, bite registration and synchronized jaw tracking.

## Next clinical substitution

Replace:

- synthetic upper arch → patient upper IOS
- synthetic lower arch → patient lower IOS
- fixed synthetic lower registration → bite/reference registration
- example CSV → synchronized patient jaw-motion CSV
- synthetic Design A → actual CAD design

The rest of the transform pipeline remains the same.
