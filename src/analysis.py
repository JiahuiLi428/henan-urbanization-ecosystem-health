"""Validation and descriptive summaries for the reported city-level indices."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


EXPECTED_YEARS = [2010, 2015, 2020, 2022]
EXPECTED_CITY_COUNT = 17
REQUIRED_COLUMNS = {
    "year",
    "city",
    "city_zh",
    "urbanisation_index_reported",
    "ecosystem_health_index_reported",
    "coupling_coordination_reported",
    "coordination_class",
}


def coordination_class(value: float) -> str:
    """Classify a value using the five thresholds stated in the report."""
    if value <= 0.2:
        return "severe imbalance"
    if value <= 0.4:
        return "moderate imbalance"
    if value <= 0.6:
        return "basic coordination"
    if value <= 0.8:
        return "moderate coordination"
    return "high coordination"


def load_data(path: str | Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    validate_data(data)
    return data


def validate_data(data: pd.DataFrame) -> dict[str, float | int]:
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {sorted(missing_columns)}")
    if data.duplicated(["year", "city"]).any():
        raise ValueError("Duplicate city-year records found")
    if sorted(data["year"].unique().tolist()) != EXPECTED_YEARS:
        raise ValueError("Unexpected study years")
    if data["city"].nunique() != EXPECTED_CITY_COUNT:
        raise ValueError("Unexpected city count")
    if len(data) != EXPECTED_CITY_COUNT * len(EXPECTED_YEARS):
        raise ValueError("The city-year panel is incomplete")
    counts = data.groupby("city")["year"].nunique()
    if not counts.eq(len(EXPECTED_YEARS)).all():
        raise ValueError("At least one city is missing a study year")

    numeric = [
        "urbanisation_index_reported",
        "ecosystem_health_index_reported",
        "coupling_coordination_reported",
    ]
    if data[numeric].isna().any().any():
        raise ValueError("Missing numeric values found")
    if not data["coupling_coordination_reported"].between(0, 1).all():
        raise ValueError("Coupling-coordination values must lie between zero and one")
    if not (data[["urbanisation_index_reported", "ecosystem_health_index_reported"]] > 0).all().all():
        raise ValueError("Reported system indices must be positive")

    recalculated = data["coupling_coordination_reported"].map(coordination_class)
    if not recalculated.eq(data["coordination_class"]).all():
        raise ValueError("Coordination classes do not match the stated thresholds")

    return {
        "rows": len(data),
        "cities": data["city"].nunique(),
        "years": data["year"].nunique(),
    }


def provincial_summary(data: pd.DataFrame) -> pd.DataFrame:
    metrics = [
        "urbanisation_index_reported",
        "ecosystem_health_index_reported",
        "coupling_coordination_reported",
    ]
    summary = data.groupby("year", as_index=False)[metrics].mean()
    for metric in metrics:
        summary[f"{metric}_index_2010"] = 100 * summary[metric] / summary.loc[0, metric]
    return summary


def city_coupling_change(data: pd.DataFrame) -> pd.DataFrame:
    wide = data.pivot(index="city", columns="year", values="coupling_coordination_reported")
    result = wide.reset_index()
    result["change_2010_2022"] = result[2022] - result[2010]
    result["relative_change_pct"] = 100 * result["change_2010_2022"] / result[2010]
    return result.sort_values("change_2010_2022", ascending=False).reset_index(drop=True)


def class_counts(data: pd.DataFrame) -> pd.DataFrame:
    counts = (
        data.groupby(["year", "coordination_class"])
        .size()
        .rename("cities")
        .reset_index()
    )
    return counts
