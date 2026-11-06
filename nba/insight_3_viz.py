"""Visualization for Insight 3: NBA close games."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd


def plot_close_game_trend(
    trend: pd.DataFrame,
    output_path: str | Path = "figures/insight_3_close_game_rate.png",
) -> Figure:
    """
    Plot the percentage of close NBA games by season.

    Parameters
    ----------
    trend : pandas.DataFrame
        Season-level close-game statistics.
    output_path : str or Path
        Location for the saved figure.

    Returns
    -------
    matplotlib.figure.Figure
        The resulting chart.
    """
    if trend.empty:
        raise ValueError("The input DataFrame is empty.")

    series = trend.set_index("season_start_year")[
        "close_game_pct"
    ].sort_index()

    years = range(
        int(series.index.min()),
        int(series.index.max()) + 1,
    )
    series = series.reindex(years)

    x_values: list[int] = [int(year) for year in series.index]
    y_values: list[float] = [
        float(value) for value in series.to_numpy(dtype=float)
    ]

    fig, ax = plt.subplots(figsize=(11, 5))

    ax.plot(
        x_values,
        y_values,
        marker="o",
        linewidth=2,
        markersize=3,
    )

    ax.set_title("How common are close NBA games?", fontsize=14)
    ax.set_xlabel("Season starting year")
    ax.set_ylabel("Games decided by 5 points or fewer (%)")
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.3)

    if 2012 in series.index and pd.isna(series.loc[2012]):
        ax.axvspan(2011.5, 2012.5, alpha=0.15)
        ax.annotate(
            "2012-13 missing",
            xy=(2012, ax.get_ylim()[1] * 0.9),
            ha="center",
            fontsize=9,
        )

    fig.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path, dpi=180)

    return fig
