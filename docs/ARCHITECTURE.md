# Architecture

## 1. Capture layer

Patient video + IOS + optional bite/CBCT/jaw tracking.

## 2. Tracking layer

Estimate per-frame head pose, FLAME expression and jaw parameters using VHAP or another compatible tracker.

## 3. Avatar layer

Expose a common interface so we can benchmark multiple backends:

- GaussianAvatars
- FlashAvatar
- MeGA
- GaussianBlendshapes
- SplattingAvatar

## 4. Dental geometry layer

Maintain real metric meshes for:

- maxillary dentition
- mandibular dentition
- gingiva where available
- proposed restorative/smile design

## 5. Registration layer

Transforms:

- `T_face_to_world`
- `T_upper_to_face`
- `T_lower_to_mandible`
- `T_design_to_upper`

Upper dentition is effectively skull-fixed. Lower dentition follows a separate mandibular transform.

## 6. Renderer

Composite photorealistic facial representation with rasterized/mesh-rendered dental geometry using a consistent camera and depth model.

## 7. Analytics

Potential metrics per frame:

- maxillary incisor display
- gingival display
- smile arc
- dental midline vs facial midline
- occlusal/incisal cant
- buccal corridor
- tooth visibility
- lip-to-incisor distance
- upper/lower lip trajectory
- design visibility through speech/smile cycle
