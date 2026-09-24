# Teeth3DS / 3DTeethSeg Integration

The public 3DTeethSeg/Teeth3DS benchmark provides 1,800 intraoral scans from
900 patients. Upper and lower jaws are provided separately.

For each OBJ scan, the corresponding JSON file contains:

- `id_patient`
- `jaw`
- one FDI `label` per vertex
- one tooth `instance` id per vertex

Label/instance `0` denotes gingiva.

Dataset source:
https://github.com/abenhamadou/3DTeethSeg_MICCAI_Challenges

The source repository states that the dataset is licensed under
**CC BY-NC-ND 4.0**. Therefore this project does not redistribute meshes or
derived dataset files.

## Local workflow

After downloading the dataset from its official source, keep it outside Git.

Example:

```bash
python scripts/prepare_teeth3ds_case.py \
  --obj /secure/teeth3ds/<case>.obj \
  --json /secure/teeth3ds/<case>.json \
  --teeth 13 12 11 21 22 23
```

The script validates that the per-vertex metadata matches the OBJ, then writes
a local anterior submesh for integration testing.

## Why anterior selection first?

The first smile-design proof of concept only needs the visible maxillary
esthetic zone. Starting with 13–23:

- reduces rendering complexity,
- simplifies registration,
- directly targets veneers/crowns/smile design,
- allows faster occlusion debugging.

Once stable, expand to 17–27 and then add the lower arch.

## Registration plan

1. Load the selected upper scan.
2. Preserve original metric scale.
3. Identify dental anchors.
4. Estimate `T_upper_to_face`.
5. Replay the full VHAP sequence.
6. Measure temporal dental drift.
7. Compare original mesh vs proposed CAD design using the same transform chain.
