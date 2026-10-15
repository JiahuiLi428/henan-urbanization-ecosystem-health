# Processed data dictionary

`henan_city_system_indices_2010_2022.csv` contains one row per city and study year.

| Column | Meaning |
|---|---|
| `year` | Study year: 2010, 2015, 2020 or 2022 |
| `city` | English city name |
| `city_zh` | Chinese city name as normalised from the report |
| `urbanisation_index_reported` | New-urbanisation value reproduced from Table 3; source scale retained |
| `ecosystem_health_index_reported` | Ecosystem-health value reproduced from Table 4; source scale retained |
| `coupling_coordination_reported` | Coupling-coordination value reproduced from Table 5 |
| `coordination_class` | Class calculated from the five thresholds stated in the report's methods |

The source report is not included because it contains names, phone numbers and institutional form content. See the repository data-quality audit for known inconsistencies.
