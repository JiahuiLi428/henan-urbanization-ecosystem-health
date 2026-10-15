from pathlib import Path

import pandas as pd
import pytest

from src.analysis import city_coupling_change, load_data, provincial_summary


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "henan_city_system_indices_2010_2022.csv"


def test_panel_is_complete() -> None:
    data = load_data(DATA_PATH)
    assert len(data) == 68
    assert data["city"].nunique() == 17
    assert sorted(data["year"].unique().tolist()) == [2010, 2015, 2020, 2022]


def test_reported_coordination_range() -> None:
    data = load_data(DATA_PATH)
    assert data["coupling_coordination_reported"].between(0, 1).all()


def test_documented_change_counts() -> None:
    data = load_data(DATA_PATH)
    changes = city_coupling_change(data)
    assert (changes["change_2010_2022"] > 0).sum() == 14
    assert (changes["change_2010_2022"] < 0).sum() == 3


def test_provincial_means_match_reported_values() -> None:
    data = load_data(DATA_PATH)
    summary = provincial_summary(data).set_index("year")
    assert summary.loc[2010, "coupling_coordination_reported"] == pytest.approx(0.5405882353)
    assert summary.loc[2022, "coupling_coordination_reported"] == pytest.approx(0.5994117647)
