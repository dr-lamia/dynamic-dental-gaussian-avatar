# Original-vs-Design Motion Control

The avatar motion and camera must be identical when comparing restorative
designs. Only dental geometry is allowed to change.

## Transform chain

For an upper design:

```
design mesh
→ T_design_to_upper
→ T_upper_to_face
→ T_face_to_world(frame)
→ camera
```

For lower dentition:

```
lower mesh
→ T_lower_to_mandible
→ T_mandible_to_face(frame)
→ T_face_to_world(frame)
→ camera
```

This prevents a common visual-simulation problem: accidentally changing facial
pose, viewpoint, or timing when comparing two smile designs.

## Synthetic demonstration

Run:

```bash
python scripts/create_design_swap_demo.py
```

It writes:

- `outputs/design_swap_demo/original.obj`
- `outputs/design_swap_demo/design_a.obj`

The demonstration modifies only anterior dental geometry while using the same
motion transform chain.

## Future patient workflow

The same structure will accept:

- original IOS
- veneer Design A
- veneer Design B
- AI-generated Design C

and replay all of them against the exact same tracked VHAP/FLAME sequence.
