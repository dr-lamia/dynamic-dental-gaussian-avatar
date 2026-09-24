# Avatar Backend Benchmark — Milestone 1

## Decision for the first executable pipeline

### Primary path: VHAP → GaussianAvatars

Why this is first:

- VHAP directly supports monocular patient video.
- VHAP exports tracked results as a NeRF/3DGS-style dataset.
- The VHAP project explicitly states that its tracking output can be used to create GaussianAvatars.
- GaussianAvatars supports FLAME-bound Gaussians and motion replay, which is useful for keeping dental meshes in a controlled facial coordinate system.
- The viewer/render scripts expose motion sequences separately from avatar appearance.

### Comparison path: FlashAvatar

Why we still test it:

- It is designed for monocular video.
- Its published repository targets fast reconstruction and very high rendering speed.
- It may be more practical for a future clinic workflow.

Why it is isolated:

- The released environment uses Python 3.7 / PyTorch 1.12.1 / CUDA 11.6.
- Our VHAP/GaussianAvatars path uses a newer Python/CUDA/PyTorch environment.
- It depends on its own metrical-tracker output and preprocessing.

### Research path: MeGA

MeGA is architecturally interesting because it combines mesh and Gaussian representations, which resembles our planned hybrid face + true dental mesh approach. It is retained as an experimental backend, but not used for the first MVP because its training pipeline is heavier and uses additional preprocessing.

## Upstream requirements observed

### VHAP
- Python 3.10
- CUDA toolkit (README example: 12.1)
- PyTorch matching CUDA
- FLAME 2023 assets
- Monocular preprocessing with Robust Video Matting
- Tracking output can be exported to a NeRF/3DGS dataset

### GaussianAvatars
- CUDA GPU, compute capability 7.0+
- README reports 11 GB VRAM as a hardware requirement
- Python 3.10
- tested with modern PyTorch/CUDA combinations
- supports FLAME-bound Gaussians
- separate training, viewer and offline rendering scripts

### FlashAvatar
- released environment: Python 3.7.13
- PyTorch 1.12.1
- CUDA toolkit 11.6
- PyTorch3D
- expects extracted frames, alpha masks, parsing output and metrical-tracker results

## Benchmark criteria

Each backend should be scored on measured values rather than impressions:

| Criterion | Metric |
|---|---|
| Patient capture burden | cameras / video duration / preprocessing |
| Reconstruction time | minutes |
| GPU memory | peak GB |
| Render speed | FPS at fixed resolution |
| Facial identity | LPIPS / SSIM / blinded rating |
| Motion control | FLAME/jaw/expression controllability |
| Dental integration | access to stable face/jaw transforms |
| Temporal stability | frame-to-frame landmark drift |
| Licensing | research vs commercial restrictions |
| Engineering complexity | setup steps / environment isolation |

## Current ranking for the *first prototype only*

1. **VHAP + GaussianAvatars** — primary implementation path.
2. **FlashAvatar** — speed/usability comparator.
3. **MeGA** — architecture experiment after the first dental mesh is integrated.

This ordering is an engineering sequence, not a claim that one method is scientifically superior. Final selection will depend on measured benchmark results.
