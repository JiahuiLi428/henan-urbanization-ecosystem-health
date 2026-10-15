# Figure contract

## Core conclusion

Reported urbanisation rose rapidly between 2010 and 2022, while ecosystem-health values were broadly flat and gains in coupling coordination were uneven across Henan cities.

## Evidence and layout

- **Archetype:** quantitative hero figure with subordinate evidence panels.
- **Backend:** Python only for drawing, previewing and export.
- **Hero evidence:** a direct city-level dumbbell comparison of the reported 2010 and 2022 coordination values, paired with three decision-relevant summary statistics.
- **Quantitative evidence:** provincial mean trajectories, city-level change, a city-year heatmap and class counts.
- **Outputs:** high-resolution PNG for GitHub and editable SVG for both generated statistical figures.

## Integrity and review risks

- The original maps are retained as provenance but are not used as the README hero because the source GIS layers are unavailable and the raster pair does not support a clean, direct comparison.
- No raw boundaries, GIS projects or raster inputs are distributed.
- Reported urbanisation and ecosystem-health scales are retained without relabelling them as normalised scores.
- The analysis is descriptive. No uncertainty intervals or causal design were available.
- Formula and coverage inconsistencies in the source materials are documented rather than silently repaired.
