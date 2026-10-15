# Methodology and public scope

## Original study design

The competition study compared reported new-urbanisation, ecosystem-health and coupling-coordination indices for Henan cities in 2010, 2015, 2020 and 2022.

The report described the urbanisation system through population, economic, spatial, social and green-development dimensions. It described ecosystem health through a VORS-related framework covering vitality, organisation, resilience and ecosystem services. The final stage applied a coupling-coordination model to compare the two systems.

## Public reproducibility

This repository starts from the three city-level result tables in the submitted report. It reproduces:

- table extraction into a tidy 17-city panel;
- schema, completeness and range checks;
- provincial mean trajectories;
- city-level 2010–2022 comparisons;
- reported coordination-class counts;
- the portfolio charts and executed notebooks.

It does not reproduce the upstream entropy weighting, GIS processing, VORS calculation or original coupling-model run. Complete raw indicators, spatial inputs, parameter decisions and a formula-consistent two-system workbook were not available for public release.

## Coordination classes

The processed data applies the five thresholds stated in the methods section:

| Reported index | Class |
|---:|---|
| 0–0.2 | Severe imbalance |
| >0.2–0.4 | Moderate imbalance |
| >0.4–0.6 | Basic coordination |
| >0.6–0.8 | Moderate coordination |
| >0.8–1.0 | High coordination |

The original maps use a different four-class legend. The source rasters are preserved as submitted and are not used to calculate the class-count chart.

## Interpretation boundary

The indices are reported study outputs, not direct physical measurements. Comparisons do not establish causal effects of urbanisation on ecosystem health. The four study years are repeated snapshots rather than a continuous annual series.
