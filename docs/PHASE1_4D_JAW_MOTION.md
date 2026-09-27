# Phase 1 — Same-Patient 4D Dental Motion Pipeline

## Objective

Build the first reproducible proof-of-concept in which the **same patient** contributes:

- facial video,
- upper IOS,
- lower IOS,
- bite registration,
- jaw-motion recording,
- and at least one proposed CAD smile/restorative design.

Public datasets are used to develop and benchmark individual modules, but unrelated public subjects must not be fused and described as a patient-specific digital twin.

## Coordinate-system model

Use the facial/maxillary coordinate system as the stable reference.

For video frame (t):

```text
upper_world(t)  = face_to_world(t) · upper_to_face · upper_vertices

lower_world(t)  = face_to_world(t)
                  · mandible_to_face(t)
                  · lower_to_mandible
                  · lower_vertices

design_world(t) = face_to_world(t)
                  · upper_to_face
                  · design_to_upper
                  · design_vertices
```

This keeps the maxillary dentition rigid with the head while allowing the mandible to move independently.

## Standard jaw-motion interchange format

The project now supports CSV input with:

```text
frame_index
timestamp_s                       (optional)
tx_mm, ty_mm, tz_mm
qw, qx, qy, qz                   # preferred
jaw_opening_mm                   (optional)
```

It also accepts:

- `rx_deg, ry_deg, rz_deg` instead of quaternion rotation, or
- a complete homogeneous transform `m00 ... m33`.

The transform must represent **mandible → face/maxillary coordinates**.

## Tracker adapters

Tracker-specific outputs should be converted to the neutral CSV before rendering. Candidate sources include:

- open optical jaw tracking such as JawTrackingSystem,
- video-marker/smartphone tracking,
- commercial axiography/jaw-tracking exports where permitted,
- research sensor systems.

Do not assume that two trackers use the same axis directions, origin, units or quaternion order. Document and validate every conversion.

## Synchronization

The jaw sequence and facial video should contain a shared event or synchronized clock.

Preferred order:

1. hardware timestamp synchronization;
2. shared trigger/event marker;
3. visible instructed event such as one deliberate open-close cycle.

Resampling to the facial-video frame rate should preserve the original raw trajectory and create a derived aligned trajectory for analysis.

## Phase-1 workflow

1. Record 30–60 s facial video.
2. Acquire upper/lower IOS and bite.
3. Record jaw motion with opening/closing, protrusion/retrusion and right/left excursions.
4. Track the face with VHAP/FLAME or the selected backend.
5. Convert jaw output to the standardized CSV.
6. Register upper IOS to the facial/maxillary coordinate system.
7. Register lower IOS to the mandibular coordinate system.
8. Replay the same facial and mandibular motion with:
   - original dentition,
   - design A,
   - optional design B/C.
9. Export synchronized renders and quantitative metrics.

## Minimum validation outputs

### Registration
- landmark RMSE in mm
- surface-to-surface distance where reference geometry permits

### Temporal stability
- frame-to-frame upper-dental drift relative to the face
- lower-dental trajectory continuity
- transform discontinuities / outlier frames

### Functional motion
- maximum opening
- protrusive displacement
- right/left lateral excursion
- trajectory repeatability across repeated movements

### Smile-design analysis
- maxillary incisor display
- lip-to-incisal-edge distance
- dental midline relative to facial midline
- design visibility through the same motion sequence

## First engineering success criterion

One patient should show:

1. a stable tracked face,
2. a stable upper IOS fixed to the maxilla,
3. a lower IOS following measured jaw motion,
4. a replaceable anterior CAD design,
5. the same motion replayed for original and proposed designs,
6. no visually obvious frame-to-frame dental drift.

## Research endpoint

A suitable first methods paper can evaluate whether the integrated system reproduces reference dental/jaw measurements with acceptable spatial and temporal error. A later dataset paper can report the same-patient multimodal cohort once enough cases are prospectively collected.
