# Environment Strategy

Use separate environments for upstream avatar projects.

## Environment A — VHAP

Follow the VHAP repository installation. The current upstream README uses Python 3.10 and demonstrates CUDA 12.1 + matching PyTorch.

## Environment B — GaussianAvatars

Follow the GaussianAvatars installation. Its current documentation lists Python 3.10 and tested CUDA/PyTorch combinations. Keep it separate from VHAP initially even if versions can overlap.

## Environment C — FlashAvatar

Keep isolated because the released `environment.yml` pins Python 3.7.13, PyTorch 1.12.1 and CUDA toolkit 11.6.

## Our orchestration environment

The present repository should remain lightweight. It stores manifests, transforms, metrics and adapters and invokes upstream projects through their own environments. Do not install incompatible CUDA stacks into one environment.
