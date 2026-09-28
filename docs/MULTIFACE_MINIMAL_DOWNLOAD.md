# Minimal MultiFace Download for the 4D Dental Prototype

This configuration downloads only the assets needed for the first facial-motion benchmark.

## Identity

- `6795937`
- This is the same identity used by the official MultiFace `mini_download_config.json`.

## Assets enabled

- tracked meshes: **yes**
- metadata: **yes**
- raw camera images: **no**
- unwrapped textures: **no**
- audio: **no**

Tracked-mesh folders contain per-frame `.obj` meshes and `*_transform.txt` head-pose files.

## Expressions

The initial dental subset uses:

1. `E001_Neutral_Eyes_Open`
2. `E009_Smile_Mouth_Open`
3. `E029_Show_All_Teeth`

These give a neutral baseline plus two expressions where the dentition is visible.

## Download

Clone the official MultiFace repository:

```bash
git clone https://github.com/facebookresearch/multiface
cd multiface
pip install -r requirements.txt
```

Copy this repository's config file:

```text
configs/multiface_dental_minimal.json
```

into the MultiFace folder, then run:

```bash
python download_dataset.py \
  --dest "D:/MultiFace-dental-minimal" \
  --download_config "./multiface_dental_minimal.json"
```

Change the destination path as needed.

## Expected size

The official MultiFace mini dataset is 16.2 GB because it includes raw images, meshes, textures, metadata and audio for two expressions.

This dental-minimal configuration disables the largest asset classes: raw multi-camera images and textures. Therefore it should be **substantially smaller than 16.2 GB**, but the official repository does not publish an exact byte size for this custom combination. Treat the final download size reported by the downloader/server as authoritative.

## Optional ultra-small first test

For the smallest possible proof of concept, keep only:

```json
"expression": ["E009_Smile_Mouth_Open"]
```

This is enough to verify the tracked-mesh/head-pose ingestion pipeline before adding the neutral and teeth-showing sequences.
