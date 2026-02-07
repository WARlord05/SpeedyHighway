"""
Analytics module for SpeedyHighway game data.
Provides schema validation, summary statistics, and analysis utilities.
"""

from .schema import validate_game_data, get_schema_errors
from .summary_stats import compute_summary_stats

__all__ = ["validate_game_data", "get_schema_errors", "compute_summary_stats"]
