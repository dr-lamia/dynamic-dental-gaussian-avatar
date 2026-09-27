# First Same-Patient 4D Dental Case — Capture Checklist

This is the minimum practical pack for the first real patient-specific proof of concept.

## 1. Governance first

Before capture:

- use a pseudonymous research ID such as `P001`; do not use the patient's name in filenames
- obtain the required institutional ethics/consent approvals for facial video, dental scans and motion data
- store identifiable source data in institutionally approved storage, not in this public repository
- acquire CBCT only when independently clinically indicated and ethically permitted

## 2. Required files

Create one secure folder for the case:

```text
P001/
├── facial_video.mp4
├── upper_ios.stl
├── lower_ios.stl
├── bite.stl
├── jaw_motion.csv
├── design_A.stl
└── case.json
```

Optional later additions:

```text
facial_scan.ply
design_B.stl
design_C.stl
CBCT_DICOM/
photos/
follow_up/
```

## 3. Facial video

Use a stable camera/phone position and fixed lighting.

Capture:

1. neutral/rest
2. natural social smile
3. maximum smile
4. slow mouth opening and closing
5. slow head turn left/right
6. short standardized speech segment

For research consistency, keep camera position, zoom, lighting and patient position as constant as possible. Prefer a high frame rate when available because jaw/facial synchronization is easier with denser temporal sampling.

## 4. Dental scans

Acquire:

- upper intraoral scan
- lower intraoral scan
- buccal bite/occlusal registration

Export in `.stl`, `.ply` or `.obj` without rescaling. Preserve metric units and document the scanner/software version separately in the study log.

## 5. Jaw-motion capture

Use the selected approved optical/video/jaw-tracking method.

Record at least three repetitions of:

1. opening/closing
2. protrusion/retrusion
3. right lateral excursion
4. left lateral excursion

The raw tracker output should be converted to the project's standardized CSV:

```text
frame_index,timestamp_s,tx_mm,ty_mm,tz_mm,qw,qx,qy,qz,jaw_opening_mm
```

A full 4×4 matrix or Euler XYZ format is also accepted.

## 6. Synchronization

Include a shared synchronization event visible/identifiable in both facial and jaw-motion streams.

A simple protocol is:

1. start facial recording
2. start jaw-motion recording
3. perform one deliberate open-close event
4. pause briefly
5. begin the standardized movement sequence

Keep raw timing information. Do not overwrite original timestamps during later resampling.

## 7. Smile design

Export at least one actual CAD proposal:

```text
design_A.stl
```

For comparative research, additional designs can be added as `design_B.stl`, `design_C.stl`, etc.

## 8. Create the case manifest

Copy:

```text
examples/real_case_manifest.template.json
```

into the secure patient folder and rename it:

```text
case.json
```

Edit only the filenames and pseudonymous case ID.

## 9. Validate before processing

From the repository root:

```bash
python scripts/validate_case_inputs.py /secure/path/P001/case.json
```

The validator checks:

- expected file types
- whether every referenced file exists
- file size
- whether the jaw-motion CSV can be parsed
- frame count
- duration
- path length
- maximum displacement
- maximum rotation
- maximum supplied jaw opening

A valid case returns:

```json
{
  "ready": true
}
```

If something is missing, it returns `ready: false` and names the missing input.

## 10. First-case acceptance criteria

The first case is ready for 4D integration when:

- upper and lower IOS load correctly
- bite/reference registration is available
- facial video is usable for tracking
- jaw-motion CSV parses without errors
- jaw and facial streams contain a synchronization event
- at least one CAD design is available
- all files belong to the **same patient and same acquisition episode** or are explicitly documented if acquired at separate clinically justified sessions

## Do not upload the patient folder to public GitHub

The repository should contain only code, templates, synthetic examples and non-identifiable research outputs that are approved for release.
