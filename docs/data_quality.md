# Data-quality audit

## Canonical public panel

The public CSV reproduces Tables 3–5 of the submitted report: 17 cities × 4 years = 68 city-year observations. Values are preserved at the precision shown in those tables.

## Material inconsistencies found

1. **City coverage.** The result tables state that Jiyuan lacks data and contain 17 cities. The source workbook and map discussion include Jiyuan, producing an 18-city scope elsewhere. The public panel follows the formal result tables and excludes Jiyuan.
2. **Formula definition.** The report describes a two-system coupling model with equal weights of 0.5 and 0.5. The available workbook calculates coupling across three composite functions and uses 0.3, 0.3 and 0.4 in the evaluation index. The reported values are therefore treated as published outcomes, not as a fully reproduced two-system calculation.
3. **Year labels.** Workbook sheets named 2015, 2017, 2019 and 2021 match the report's 2010, 2015, 2020 and 2022 tables after rounding. The raw-year provenance cannot be independently reconstructed from the public-ready files.
4. **Index scales.** The methods describe ecosystem health on a 0–1 scale, while the result table reports values from roughly 23 to 97. The CSV therefore uses the suffix `_reported` and does not reinterpret the units.
5. **Trend statement.** The report says coupling coordination increased for all cities from 2010 to 2022. The table shows increases in 14 cities and declines in Xuchang, Xinyang and Shangqiu. The provincial mean also falls slightly from 0.603 in 2020 to 0.599 in 2022.
6. **Top cities.** The abstract highlights Zhengzhou and Luoyang at about 0.7 in 2022. The table gives Zhengzhou 0.71, Luoyang 0.70 and Nanyang 0.70.
7. **Map classes.** The methods state five coordination classes, while the supplied maps show four. Generated statistical outputs use the five written thresholds; source maps retain their original legend.

## Corrections and non-corrections

The repository corrects only derived summaries that can be recalculated directly from the reported tables. It does not alter the submitted city values, infer missing Jiyuan entries, rescale system indices or replace the original coupling formula.
