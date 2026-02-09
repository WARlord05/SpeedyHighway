"""
Analytics module for SpeedyHighway game data.
Provides schema validation, summary statistics, and analysis utilities.
"""

from .exploratory import (
    export_high_scores_csv,
    export_summary_csv,
    run_validation,
    try_plot_score_distribution,
)
from .schema import DIFFICULTY_NAMES, get_schema_errors, validate_game_data
from .summary_stats import compute_summary_stats

__all__ = [
    "validate_game_data",
    "get_schema_errors",
    "compute_summary_stats",
    "DIFFICULTY_NAMES",
    "export_high_scores_csv",
    "export_summary_csv",
    "run_validation",
    "try_plot_score_distribution",
]
