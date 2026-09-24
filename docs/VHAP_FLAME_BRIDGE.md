# VHAP / FLAME Mouth-Region Bridge

Inspection of the current upstream VHAP implementation confirms that its
`FlameMask` exposes ordered named vertex regions including:

- `lip_outside_ring_upper`
- `lip_outside_ring_lower`

VHAP itself uses those lip regions when constructing its optional proxy teeth.
That is useful for us because the same tracked lip-ring geometry can define the
mouth aperture for our **real dental mesh**, without relying on hard-coded 2D
landmark indices.

## Planned runtime bridge

Inside a VHAP environment:

1. evaluate the tracked FLAME mesh for frame *t*,
2. obtain ordered vertex IDs for the two lip-ring regions through VHAP's
   `FlameMask.get_vid_by_region(..., keep_order=True)`,
3. project those 3D vertices with the tracked camera,
4. pass the resulting upper/lower 2D rings to
   `src.tracking.vhap_flame_regions.mouth_polygon_from_rings`,
5. rasterize that polygon into the mouth mask,
6. combine the mask with face/dental depth maps in the hybrid compositor.

## Why region-based extraction is preferable

- It follows the deformed FLAME lips directly.
- It changes with jaw opening and facial expression.
- It avoids assuming a particular external 68/98/106-point landmark indexing
  convention.
- It uses the same geometric representation that VHAP actually optimizes.

## Important note

The exact VHAP/FLAME vertex indices are intentionally **not copied** into this
repository. They should be queried from the locally installed, licensed FLAME
assets through VHAP's own mask API.

## Related upstream behavior

The current VHAP source also exposes a `jaw_pose` parameter and its export
utility demonstrates an open-mouth state by setting jaw rotation. That supports
our planned separation between:

- maxillary teeth fixed to the facial/skull frame, and
- mandibular teeth driven by a separate jaw transform.
