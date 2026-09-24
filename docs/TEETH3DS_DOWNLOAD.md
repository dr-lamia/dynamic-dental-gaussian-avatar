# Teeth3DS Download / Local Setup

Use the **official Teeth3DS / 3DTeethSeg source** for dataset access and terms:

https://github.com/abenhamadou/3DTeethSeg_MICCAI_Challenges

The official repository currently states:

- 1,800 3D intraoral scans
- 900 patients
- upper and lower jaws separately
- OBJ surface meshes
- paired JSON per-vertex FDI labels and instances
- dataset license: CC BY-NC-ND 4.0
- dataset download is split into multiple parts and linked from the official
  repository via OSF

## Recommended local layout

Do not place the dataset inside this Git repository.

Example:

```
/secure/datasets/teeth3ds/
    3D_scans_per_patient_obj_files/
        <PATIENT_ID>/
            <PATIENT_ID>_upper.obj
            <PATIENT_ID>_lower.obj
    ground-truth_labels_instances/
        <PATIENT_ID>/
            <PATIENT_ID>_upper.json
            <PATIENT_ID>_lower.json
```

## Automatically select the first usable upper case

```bash
python scripts/find_teeth3ds_case.py \
  --root /secure/datasets/teeth3ds
```

The script writes:

```
outputs/selected_teeth3ds_case.json
```

with the paired OBJ and JSON paths.

## Prepare the anterior esthetic zone

```bash
python scripts/prepare_teeth3ds_case.py \
  --obj /path/to/<PATIENT>_upper.obj \
  --json /path/to/<PATIENT>_upper.json \
  --teeth 13 12 11 21 22 23
```

This is the real-mesh replacement for our procedural synthetic arch.

## Why we do not auto-download from an unofficial mirror

A separate dental 3DGS repository provides a convenience download script, but
its dataset-size/license description differs from the current official
Teeth3DS repository. To keep the research provenance defensible, this project
uses the official dataset record and does not silently download or redistribute
third-party mirrors.
