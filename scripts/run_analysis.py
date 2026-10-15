"""Validate the processed panel and rebuild the portfolio figure."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis import city_coupling_change, load_data, provincial_summary
from src.visualization import make_portfolio_figure, make_readme_hero


def main() -> None:
    data_path = PROJECT_ROOT / "data" / "processed" / "henan_city_system_indices_2010_2022.csv"
    output_dir = PROJECT_ROOT / "outputs" / "charts"
    data = load_data(data_path)
    summary = provincial_summary(data)
    changes = city_coupling_change(data)
    outputs = (*make_readme_hero(data, output_dir), *make_portfolio_figure(data, output_dir))

    print(f"Validated {len(data)} records for {data['city'].nunique()} cities")
    print(summary.to_string(index=False))
    print(f"Cities with higher 2022 coordination than 2010: {(changes['change_2010_2022'] > 0).sum()}")
    print("Created:")
    for path in outputs:
        print(f"  {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
