"""Build the three compact portfolio notebooks."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"


def notebook(title: str, introduction: str, cells: list) -> nbf.NotebookNode:
    document = nbf.v4.new_notebook()
    document["cells"] = [nbf.v4.new_markdown_cell(f"# {title}\n\n{introduction}"), *cells]
    document["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    }
    return document


def main() -> None:
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    setup = nbf.v4.new_code_cell(
        "from pathlib import Path\n"
        "import sys\n"
        "import pandas as pd\n\n"
        "ROOT = Path.cwd()\n"
        "if ROOT.name == 'notebooks':\n"
        "    ROOT = ROOT.parent\n"
        "sys.path.insert(0, str(ROOT))\n"
        "DATA_PATH = ROOT / 'data' / 'processed' / 'henan_city_system_indices_2010_2022.csv'"
    )

    validation = notebook(
        "Data validation",
        "Check the structure, completeness and stated coordination classes of the public 17-city panel.",
        [
            setup,
            nbf.v4.new_code_cell(
                "from src.analysis import load_data, validate_data\n\n"
                "data = load_data(DATA_PATH)\n"
                "validate_data(data)"
            ),
            nbf.v4.new_code_cell(
                "pd.crosstab(data['year'], data['coordination_class']).rename_axis(columns='class')"
            ),
            nbf.v4.new_markdown_cell(
                "The panel contains 17 cities for each of four study years. Classes are recalculated from the five thresholds written in the report rather than copied from the four-class map legend."
            ),
        ],
    )

    temporal = notebook(
        "Temporal comparison",
        "Compare provincial means while retaining the source report's original index scales.",
        [
            setup,
            nbf.v4.new_code_cell(
                "from src.analysis import load_data, provincial_summary\n\n"
                "data = load_data(DATA_PATH)\n"
                "summary = provincial_summary(data)\n"
                "summary"
            ),
            nbf.v4.new_code_cell(
                "start = summary.set_index('year').loc[2010]\n"
                "end = summary.set_index('year').loc[2022]\n"
                "pd.Series({\n"
                "    'urbanisation_change_pct': 100 * (end['urbanisation_index_reported'] / start['urbanisation_index_reported'] - 1),\n"
                "    'ecosystem_health_change_pct': 100 * (end['ecosystem_health_index_reported'] / start['ecosystem_health_index_reported'] - 1),\n"
                "    'coupling_change_points': end['coupling_coordination_reported'] - start['coupling_coordination_reported'],\n"
                "}).round(3)"
            ),
            nbf.v4.new_markdown_cell(
                "Urbanisation rose strongly, ecosystem-health values were broadly flat to slightly lower, and mean coupling coordination improved overall but dipped slightly after 2020."
            ),
        ],
    )

    city = notebook(
        "City comparison",
        "Identify where the reported coupling-coordination index improved or declined between 2010 and 2022.",
        [
            setup,
            nbf.v4.new_code_cell(
                "from src.analysis import city_coupling_change, load_data\n\n"
                "data = load_data(DATA_PATH)\n"
                "changes = city_coupling_change(data)\n"
                "changes"
            ),
            nbf.v4.new_code_cell(
                "pd.Series({\n"
                "    'cities_improved': int((changes['change_2010_2022'] > 0).sum()),\n"
                "    'cities_declined': int((changes['change_2010_2022'] < 0).sum()),\n"
                "    'largest_gain_city': changes.iloc[0]['city'],\n"
                "    'largest_gain': changes.iloc[0]['change_2010_2022'],\n"
                "}).to_frame('result')"
            ),
            nbf.v4.new_markdown_cell(
                "The table contradicts the report's statement that every city improved: Xuchang, Xinyang and Shangqiu are lower in 2022 than in 2010."
            ),
        ],
    )

    outputs = {
        "01_data_validation.ipynb": validation,
        "02_temporal_comparison.ipynb": temporal,
        "03_city_comparison.ipynb": city,
    }
    for filename, document in outputs.items():
        nbf.write(document, NOTEBOOK_DIR / filename)
        print(NOTEBOOK_DIR / filename)


if __name__ == "__main__":
    main()
