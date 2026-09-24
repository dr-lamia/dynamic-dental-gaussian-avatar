# Dental Registration — MVP

## Objective

Place the real upper/lower IOS and CAD smile design in the same coordinate
system as the tracked face while preserving true dental scale.

## First implementation

Use at least three non-collinear corresponding 3D landmarks to initialize a
rigid transform. The implementation in `src/registration/rigid.py` uses an
SVD/Kabsch fit and deliberately does **not** estimate scale.

This matters because IOS geometry is metric and restorative dimensions must
not be distorted merely to improve visual alignment.

## Initial transform chain

```text
upper IOS point
  → T_upper_to_face
  → tracked face/world

design point
  → T_design_to_upper
  → T_upper_to_face
  → tracked face/world

lower IOS point
  → T_lower_to_mandible
  → T_mandible(frame)
  → tracked face/world
```

## Landmark strategy for the proof of concept

Prefer landmarks that can be reproducibly identified in both the dental and
facial/reference representation. The exact final landmark set will be chosen
after inspecting the first patient's modalities.

The workflow should save:

- source landmark coordinates
- target landmark coordinates
- 4×4 transform
- landmark RMSE
- refinement settings
- software/version information

## Next refinement

After the landmark transform, add surface-based ICP only on appropriate
overlapping geometry. Never allow unconstrained ICP to scale the dental mesh.
