# Lip–Teeth Occlusion

Correct registration is not enough. If the dental renderer ignores the facial
surface, teeth can appear through the lips or cheeks.

## MVP rule

A dental pixel is visible only when:

1. it lies inside the detected/projected mouth opening, and
2. its depth is in front of the facial depth at the same pixel.

Conceptually:

```
visible_teeth = mouth_opening
                AND dental_surface_exists
                AND dental_depth <= face_depth
```

## Inputs per frame

- face RGB render
- face depth map
- dental RGB render
- dental depth map
- mouth-opening mask

## Mouth mask

For the first implementation, the mouth opening can be represented by a 2D
polygon from projected lip landmarks.

Later, when VHAP/FLAME integration is running, the mask should be generated
directly from tracked lip landmarks or a facial semantic mask.

## Why this matters

Without depth-aware occlusion:

- upper incisors may draw over the upper lip,
- posterior teeth may show through cheeks,
- mandibular teeth may remain visible during lip closure.

That would make the dynamic smile-design simulation visually misleading even
if the 3D transform is numerically correct.

## Next refinement

After the public avatar run:

1. inspect VHAP/FLAME lip landmark indices,
2. project them into each camera frame,
3. generate a mouth-opening polygon,
4. request/render a face depth map,
5. composite dental geometry with the visibility mask,
6. compare against the original video frame.

Longer term, add soft alpha blending and local depth bias around the lip margin
to avoid rasterization-edge artifacts.
