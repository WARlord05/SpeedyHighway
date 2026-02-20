"""
Exploratory data analysis utilities for SpeedyHighway game data.
Provides CSV export and optional visualizations (when pandas/matplotlib available).
"""

import csv
from pathlib import Path
from typing import Any

from .schema import get_schema_errors
from .summary_stats import compute_summary_stats

# CSV column order for high_scores export
HIGH_SCORES_CSV_COLUMNS = ["score", "difficulty", "survival_time", "date"]


def export_high_scores_csv(data: dict, output_path: str | Path) -> None:
    """
    Export high_scores from game_data to a CSV file.
    Uses standard library only; safe to call without pandas.
    """
    output_path = Path(output_path)
    high_scores = data.get("high_scores") or []
    if not high_scores:
        output_path.write_text("score,difficulty,survival_time,date\n", encoding="utf-8")
        return
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HIGH_SCORES_CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for entry in high_scores:
            if isinstance(entry, dict):
                row = {k: entry.get(k, "") for k in HIGH_SCORES_CSV_COLUMNS}
                writer.writerow(row)
    return None


def export_summary_csv(stats: dict[str, Any], output_path: str | Path) -> None:
    """
    Export summary statistics to a two-column CSV (metric, value).
    Uses standard library only.
    """
    output_path = Path(output_path)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, value in stats.items():
            if isinstance(value, dict):
                continue  # Skip nested dicts for flat CSV
            writer.writerow([key, value])
    return None


def run_validation(data: dict) -> tuple[bool, list[str]]:
    """
    Run schema validation on game_data.
    Returns (is_valid, list of error messages).
    """
    errors = get_schema_errors(data)
    return (len(errors) == 0, errors)


def try_plot_score_distribution(data: dict, save_path: str | Path | None = None) -> bool:
    """
    If pandas and matplotlib are available, plot score distribution and optionally save.
    Returns True if plot was generated, False if dependencies missing or no scores.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    high_scores = data.get("high_scores") or []
    scores = [e["score"] for e in high_scores if isinstance(e, dict) and "score" in e]
    if not scores:
        return False
    fig, ax = plt.subplots()
    ax.hist(scores, bins=min(20, max(1, len(scores))), edgecolor="black", alpha=0.7)
    ax.set_xlabel("Score")
    ax.set_ylabel("Count")
    ax.set_title("SpeedyHighway – High score distribution")
    plt.tight_layout()
    if save_path:
        fig.savefig(Path(save_path), dpi=100)
    plt.close()
    return True
