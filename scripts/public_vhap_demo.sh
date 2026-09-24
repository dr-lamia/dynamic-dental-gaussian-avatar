#!/usr/bin/env bash
set -euo pipefail

SEQUENCE_FILE="${1:-obama.mp4}"
SEQUENCE="${SEQUENCE_FILE%.*}"
DATA_ROOT="${VHAP_DATA_ROOT:-data/monocular}"
TRACK_OUTPUT="${VHAP_TRACK_OUTPUT:-output/monocular/${SEQUENCE}_whiteBg_staticOffset}"
EXPORT_OUTPUT="${VHAP_EXPORT_OUTPUT:-export/monocular/${SEQUENCE}_whiteBg_staticOffset_maskBelowLine}"

echo "[1/3] Preprocess public monocular video"
python vhap/preprocess_video.py   --input "${DATA_ROOT}/${SEQUENCE_FILE}"   --matting_method robust_video_matting   --downsample_scales 2

echo "[2/3] Track FLAME"
python vhap/track.py   --data.root_folder "${DATA_ROOT}"   --exp.output_folder "${TRACK_OUTPUT}"   --data.sequence "${SEQUENCE}"   --data.n_downsample_rgb 2

echo "[3/3] Export NeRF/3DGS-style dataset"
python vhap/export_as_nerf_dataset.py   --src_folder "${TRACK_OUTPUT}"   --tgt_folder "${EXPORT_OUTPUT}"   --background-color white

echo "VHAP public demo export completed: ${EXPORT_OUTPUT}"
