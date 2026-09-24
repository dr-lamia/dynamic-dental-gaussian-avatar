# MVP Specification

## Patient inputs

- `video.mp4`
- `upper.stl`
- `lower.stl`
- `bite.stl` or manual alignment metadata
- `design_a.stl`

## MVP workflow

1. Track video.
2. Reconstruct/fit dynamic avatar.
3. Load IOS meshes without changing metric scale.
4. Align upper arch to the avatar.
5. Align lower arch to mandible.
6. Replace or overlay the planned anterior design.
7. Replay the same tracked motion for original and design states.
8. Export frame-level registration/visibility metrics.

## Acceptance checks

- Teeth remain stable relative to the maxilla during head movement.
- Mandibular teeth follow jaw opening rather than facial-surface deformation.
- No obvious depth-order error at the lips/teeth interface.
- Design toggle does not change camera, facial motion or timing.
- Scale and transformation matrices are stored and reproducible.
