# Interactive Alignment App

A lightweight Streamlit UI is included for the cross-subject public engineering
demo.

## Install

```bash
pip install streamlit
```

## Run

```bash
streamlit run apps/alignment_app.py
```

The UI exposes six parameters:

- translation X/Y/Z in millimeters
- rotation Rx/Ry/Rz in degrees

and saves the exact rigid transform as JSON.

## Current scope

The first UI intentionally focuses on reproducible transform control. The next
viewer revision will add a rendered face frame and dental-mesh overlay preview.

The underlying transform file remains the same, so alignment sessions created
now will remain compatible with the later viewer.
