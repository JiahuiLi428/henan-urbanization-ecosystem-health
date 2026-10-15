"""Portfolio visualisations built from the public processed dataset."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

from src.analysis import city_coupling_change, provincial_summary


PALETTE = {
    "urbanisation": "#D9822B",
    "ecosystem": "#4F8A70",
    "coordination": "#7451A6",
    "positive": "#2D6A9F",
    "negative": "#C65D38",
    "neutral": "#B9BEC5",
}


def configure_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "svg.hashsalt": "henan-coupling-portfolio",
            "pdf.fonttype": 42,
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.linewidth": 0.8,
            "legend.frameon": False,
        }
    )


def make_readme_hero(data: pd.DataFrame, output_dir: str | Path) -> tuple[Path, Path]:
    """Create a direct 2010–2022 comparison for the repository homepage."""
    configure_style()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    wide = data.pivot(index="city", columns="year", values="coupling_coordination_reported")
    wide = wide.assign(change=wide[2022] - wide[2010]).sort_values(2022, ascending=False)
    mean_2010 = data.loc[data["year"].eq(2010), "coupling_coordination_reported"].mean()
    mean_2022 = data.loc[data["year"].eq(2022), "coupling_coordination_reported"].mean()
    improved = int(wide["change"].gt(0).sum())
    declined = wide.index[wide["change"].lt(0)].tolist()

    navy = "#19324D"
    teal = "#16847B"
    coral = "#D26745"
    slate = "#8C98A4"
    pale = "#E8EDF1"
    purple = "#7562A8"

    fig = plt.figure(figsize=(14.2, 7.7), facecolor="white")
    grid = fig.add_gridspec(
        1,
        2,
        width_ratios=[3.25, 1.15],
        left=0.08,
        right=0.96,
        bottom=0.12,
        top=0.78,
        wspace=0.13,
    )

    ax = fig.add_subplot(grid[0, 0])
    positions = np.arange(len(wide))
    for y, (_, row) in zip(positions, wide.iterrows()):
        color = teal if row["change"] > 0 else coral
        ax.plot([row[2010], row[2022]], [y, y], color=color, linewidth=3.2, alpha=0.72, solid_capstyle="round")
        ax.scatter(row[2010], y, s=62, facecolor="white", edgecolor=slate, linewidth=1.8, zorder=3)
        ax.scatter(row[2022], y, s=72, facecolor=color, edgecolor="white", linewidth=0.9, zorder=4)
        label_x = max(row[2010], row[2022]) + 0.009
        ax.text(label_x, y, f"{row['change']:+.02f}", va="center", color=color, fontsize=8.2, fontweight="bold")

    ax.set_yticks(positions, labels=wide.index)
    ax.invert_yaxis()
    ax.set_xlim(0.43, 0.77)
    ax.set_xticks(np.arange(0.45, 0.76, 0.05))
    ax.set_xlabel("Reported coupling-coordination index", color="#4F5B66", labelpad=10)
    ax.grid(axis="x", color=pale, linewidth=1)
    ax.tick_params(axis="y", length=0, pad=8, labelcolor=navy)
    ax.tick_params(axis="x", colors="#65727E")
    for spine in ax.spines.values():
        spine.set_visible(False)

    legend = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markeredgecolor=slate, markeredgewidth=1.7, markersize=7, label="2010"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=teal, markeredgecolor="white", markersize=8, label="2022 · improved"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=coral, markeredgecolor="white", markersize=8, label="2022 · declined"),
    ]
    ax.legend(handles=legend, loc="lower left", bbox_to_anchor=(0, 1.025), ncol=3, handletextpad=0.5, columnspacing=1.4)

    info = fig.add_subplot(grid[0, 1])
    info.set_xlim(0, 1)
    info.set_ylim(0, 1)
    info.axis("off")
    info.axvline(0.02, color=pale, linewidth=1.2)
    info.text(0.12, 0.97, "AT A GLANCE", color="#6B7782", fontsize=9, fontweight="bold", va="top")
    info.text(0.12, 0.82, f"{improved} / 17", color=teal, fontsize=31, fontweight="bold", va="center")
    info.text(0.12, 0.74, "cities improved", color=navy, fontsize=11, fontweight="bold")

    info.text(0.12, 0.57, f"{mean_2010:.3f}", color=slate, fontsize=18, fontweight="bold")
    info.text(0.49, 0.57, "→", color="#87929C", fontsize=18, ha="center", fontweight="bold")
    info.text(0.86, 0.57, f"{mean_2022:.3f}", color=teal, fontsize=18, ha="right", fontweight="bold")
    info.text(0.12, 0.50, "provincial mean", color="#6B7782", fontsize=9)

    info.text(0.12, 0.35, "2  →  8", color=purple, fontsize=23, fontweight="bold")
    info.text(0.12, 0.27, "cities in moderate coordination", color=navy, fontsize=9.5, fontweight="bold")

    info.text(0.12, 0.12, "3 declined", color=coral, fontsize=12, fontweight="bold")
    info.text(0.12, 0.065, " · ".join(declined), color="#6B7782", fontsize=8.5)

    fig.text(0.08, 0.925, "Coordination improved — but not everywhere", color=navy, fontsize=25, fontweight="bold")
    fig.text(0.08, 0.867, "A direct city-by-city comparison of reported results in Henan, 2010–2022", color="#5F6B75", fontsize=12)
    fig.text(
        0.08,
        0.035,
        "Each line links the same city across time; labels show the absolute change. Descriptive comparison of reported values.",
        color="#6B7782",
        fontsize=8.5,
    )

    png_path = output_dir / "readme_hero.png"
    svg_path = output_dir / "readme_hero.svg"
    fig.savefig(png_path, dpi=220, facecolor="white", bbox_inches="tight", metadata={"Software": "matplotlib"})
    fig.savefig(svg_path, facecolor="white", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    return png_path, svg_path


def make_portfolio_figure(data: pd.DataFrame, output_dir: str | Path) -> tuple[Path, Path]:
    configure_style()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = provincial_summary(data)
    changes = city_coupling_change(data).sort_values("change_2010_2022")
    heatmap = data.pivot(index="city", columns="year", values="coupling_coordination_reported")
    heatmap = heatmap.sort_values(2022, ascending=False)
    counts = pd.crosstab(data["year"], data["coordination_class"])

    fig = plt.figure(figsize=(15.5, 10.8), constrained_layout=False)
    grid = fig.add_gridspec(2, 2, left=0.07, right=0.97, bottom=0.09, top=0.88, hspace=0.42, wspace=0.36)

    ax_a = fig.add_subplot(grid[0, 0])
    indexed = [
        ("urbanisation_index_reported_index_2010", "Urbanisation", PALETTE["urbanisation"]),
        ("ecosystem_health_index_reported_index_2010", "Ecosystem health", PALETTE["ecosystem"]),
        ("coupling_coordination_reported_index_2010", "Coupling coordination", PALETTE["coordination"]),
    ]
    for column, label, color in indexed:
        ax_a.plot(summary["year"], summary[column], marker="o", linewidth=2.4, markersize=6, color=color, label=label)
        ax_a.text(summary["year"].iloc[-1] + 0.25, summary[column].iloc[-1], label, color=color, va="center", fontsize=9)
    ax_a.axhline(100, color="#D9D9D9", linewidth=1, zorder=0)
    ax_a.set_title("a   Provincial mean trajectories", loc="left")
    ax_a.set_ylabel("Index (2010 = 100)")
    ax_a.set_xticks(summary["year"])
    ax_a.set_xlim(2009.4, 2026.5)
    ax_a.grid(axis="y", color="#E7E7E7", linewidth=0.8)

    ax_b = fig.add_subplot(grid[0, 1])
    colors = [PALETTE["positive"] if value >= 0 else PALETTE["negative"] for value in changes["change_2010_2022"]]
    ax_b.hlines(changes["city"], 0, changes["change_2010_2022"], color=colors, linewidth=3)
    ax_b.scatter(changes["change_2010_2022"], changes["city"], color=colors, s=42, zorder=3)
    ax_b.axvline(0, color="#626262", linewidth=0.9)
    ax_b.set_title("b   City-level coordination change", loc="left")
    ax_b.set_xlabel("Change in reported index, 2010–2022")
    ax_b.grid(axis="x", color="#E7E7E7", linewidth=0.8)
    ax_b.text(0.99, 0.02, "14 increased · 3 declined", transform=ax_b.transAxes, ha="right", va="bottom", fontweight="bold")

    ax_c = fig.add_subplot(grid[1, 0])
    cmap = LinearSegmentedColormap.from_list("coordination", ["#F4EFF8", "#B49ACB", "#644192"])
    values = heatmap.to_numpy()
    image = ax_c.imshow(values, cmap=cmap, vmin=0.4, vmax=0.75, aspect="auto")
    ax_c.set_xticks(np.arange(len(heatmap.columns)), labels=heatmap.columns)
    ax_c.set_yticks(np.arange(len(heatmap.index)), labels=heatmap.index)
    ax_c.set_xticks(np.arange(-0.5, len(heatmap.columns), 1), minor=True)
    ax_c.set_yticks(np.arange(-0.5, len(heatmap.index), 1), minor=True)
    ax_c.grid(which="minor", color="white", linewidth=0.8)
    ax_c.tick_params(which="minor", bottom=False, left=False)
    for row in range(values.shape[0]):
        for column in range(values.shape[1]):
            color = "white" if values[row, column] >= 0.64 else "#2D2633"
            ax_c.text(column, row, f"{values[row, column]:.2f}", ha="center", va="center", color=color, fontsize=7.5)
    colorbar = fig.colorbar(image, ax=ax_c, shrink=0.75, pad=0.025)
    colorbar.set_label("Reported coordination index")
    ax_c.set_title("c   City trajectories", loc="left")
    ax_c.set_xlabel("")
    ax_c.set_ylabel("")
    ax_c.tick_params(axis="y", labelsize=8)

    ax_d = fig.add_subplot(grid[1, 1])
    class_order = ["basic coordination", "moderate coordination"]
    counts = counts.reindex(columns=class_order, fill_value=0)
    bottoms = pd.Series(0, index=counts.index, dtype=float)
    class_colors = ["#CFC2DC", PALETTE["coordination"]]
    labels = ["Basic coordination", "Moderate coordination"]
    for class_name, label, color in zip(class_order, labels, class_colors):
        values = counts[class_name]
        bars = ax_d.bar(counts.index.astype(str), values, bottom=bottoms, color=color, width=0.62, label=label)
        for bar, value, bottom in zip(bars, values, bottoms):
            if value:
                ax_d.text(bar.get_x() + bar.get_width() / 2, bottom + value / 2, f"{int(value)}", ha="center", va="center", color="white" if color == PALETTE["coordination"] else "#303030", fontweight="bold")
        bottoms += values
    ax_d.set_title("d   Distribution across reported classes", loc="left")
    ax_d.set_ylabel("Number of cities")
    ax_d.set_xlabel("Year")
    ax_d.set_ylim(0, 20)
    ax_d.legend(loc="upper left", ncol=2)
    ax_d.grid(axis="y", color="#E7E7E7", linewidth=0.8)

    fig.suptitle("Urbanisation accelerated, but coordination gains were uneven", x=0.07, y=0.965, ha="left", fontsize=22, fontweight="bold")
    fig.text(0.07, 0.925, "Reported results for 17 Henan cities across four study years", fontsize=12, color="#4D4D4D")
    fig.text(0.07, 0.025, "Descriptive comparison only. Reported indices are reproduced as published; no causal inference or uncertainty intervals are available.", fontsize=8.5, color="#666666")

    png_path = output_dir / "portfolio_overview.png"
    svg_path = output_dir / "portfolio_overview.svg"
    fig.savefig(png_path, dpi=220, bbox_inches="tight", facecolor="white", metadata={"Software": "matplotlib"})
    fig.savefig(svg_path, bbox_inches="tight", facecolor="white", metadata={"Date": None})
    plt.close(fig)
    return png_path, svg_path
