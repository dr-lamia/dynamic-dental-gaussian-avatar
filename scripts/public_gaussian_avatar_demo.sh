#!/usr/bin/env bash
set -euo pipefail

SOURCE_PATH="${1:?Usage: public_gaussian_avatar_demo.sh /path/to/vhap/export [model_output]}"
MODEL_PATH="${2:-output/dental_virtual_patient_public_demo}"

python train.py   -s "${SOURCE_PATH}"   -m "${MODEL_PATH}"   --eval   --bind_to_mesh   --white_background   --port 60000

python render.py   -m "${MODEL_PATH}"   --skip_train   --skip_val

echo "GaussianAvatars public demo completed: ${MODEL_PATH}"
