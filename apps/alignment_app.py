"""Optional Streamlit alignment app for the public cross-subject demo.

Run locally:
    streamlit run apps/alignment_app.py

The app only saves transform parameters. It does not upload patient data.
"""
from pathlib import Path
import streamlit as st

from src.registration.manual_alignment import ManualAlignment
from src.registration.alignment_ui import DEFAULT_LIMITS

st.set_page_config(page_title="Dental-to-Face Alignment", layout="wide")
st.title("Dynamic Dental Avatar — Manual Alignment")
st.caption("Engineering demo only. Cross-subject public data are not anatomically registered.")

lim = DEFAULT_LIMITS

c1, c2 = st.columns(2)
with c1:
    st.subheader("Translation (mm)")
    tx = st.slider("X", lim.translation_min_mm, lim.translation_max_mm, 0.0, lim.translation_step_mm)
    ty = st.slider("Y", lim.translation_min_mm, lim.translation_max_mm, 0.0, lim.translation_step_mm)
    tz = st.slider("Z", lim.translation_min_mm, lim.translation_max_mm, 70.0, lim.translation_step_mm)

with c2:
    st.subheader("Rotation (degrees)")
    rx = st.slider("Rx", lim.rotation_min_deg, lim.rotation_max_deg, 0.0, lim.rotation_step_deg)
    ry = st.slider("Ry", lim.rotation_min_deg, lim.rotation_max_deg, 0.0, lim.rotation_step_deg)
    rz = st.slider("Rz", lim.rotation_min_deg, lim.rotation_max_deg, 0.0, lim.rotation_step_deg)

alignment = ManualAlignment(
    translation_mm=(tx, ty, tz),
    rotation_deg_xyz=(rx, ry, rz),
)

st.subheader("Transform matrix")
st.dataframe(alignment.matrix())

out = st.text_input("Output JSON", "outputs/public_demo_alignment.json")
if st.button("Save alignment"):
    path = alignment.save(Path(out))
    st.success(f"Saved: {path}")
