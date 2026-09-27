# Research Plan

## Proposed study concept

**Dynamic evaluation of 3D smile designs using a photorealistic 4D virtual patient with patient-specific mandibular motion.**

## Primary engineering question

Can a dynamic facial avatar be fused with metrically accurate intraoral geometry and measured jaw motion so that alternative dental CAD designs remain spatially stable and visually plausible throughout facial and mandibular movement?

## Validation domains

1. **Registration accuracy** — landmark/mesh distances against a reference.
2. **Temporal stability** — frame-to-frame dental pose drift.
3. **Jaw-motion fidelity** — agreement with reference opening, protrusion and lateral-excursion trajectories.
4. **Dental visibility accuracy** — predicted vs manually/reference measured tooth display.
5. **Rendering realism** — blinded clinician ratings.
6. **Design comparison repeatability** — same facial and mandibular motion, different CAD designs.
7. **Computation** — reconstruction time and rendering FPS.

## Data strategy

### Public development resources

Use public datasets to develop modules independently:

- dynamic face datasets for avatar/tracking,
- Teeth3DS and paired CBCT+IOS data for dental geometry/registration,
- public jaw-kinematics datasets for feature benchmarking,
- open jaw-tracking software for trajectory capture/processing.

Do not combine unrelated subjects from these resources and present them as one patient-specific twin.

### Same-patient validation cohort

Prospectively capture facial video + upper/lower IOS + bite + jaw motion for the same participant. Add CBCT only when clinically indicated. This cohort is the evidence base for patient-specific 4D validation.

## Suggested first paper

*A Dynamic Dental Gaussian Avatar with Patient-Specific Jaw Motion for Motion-Aware 3D Smile Design: Development and Proof-of-Concept.*

## Suggested second paper

*An Open Multimodal 4D Dental Virtual Patient Dataset: Synchronized Facial Motion, Intraoral Geometry and Mandibular Kinematics.*

The dataset-paper title should be used only if a sufficiently documented same-patient cohort is collected and ethically shareable.
