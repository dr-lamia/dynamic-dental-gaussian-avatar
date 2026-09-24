# Temporal Dental Stability

A dental mesh can look correctly positioned in one frame but drift relative to
the face during animation. The first dynamic validation therefore measures
**relative dental-to-facial drift**, not just global mesh movement.

## Principle

Whole-head movement should not count as dental drift.

For each frame:

```
relative_vector = dental_anchor - facial_anchor
```

We compare that vector with its value in the reference frame.

If the maxillary mesh is perfectly attached to the skull/face coordinate
system, the relative vector remains constant even while the patient turns or
moves.

## Report

For every sequence record:

- mean drift (mm)
- maximum drift (mm)
- 95th percentile drift (mm)
- frame number of maximum drift
- motion state at maximum drift (rest / smile / mouth opening / head turn)

## Validation use

This will become one of the core technical outcomes of the proof-of-concept:

**How stable is the patient-specific dental mesh throughout dynamic facial
motion?**

That gives us a quantitative result suitable for the methods/results section
rather than relying only on screenshots.
