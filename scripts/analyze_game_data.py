#!/usr/bin/env python3
"""
SpeedyHighway Game Data Analysis Script.
Loads game_data.json (or sample fixture), validates schema, and prints summary stats.
Run from repo root: python scripts/analyze_game_data.py [path_to_game_data.json]
"""

import json
import os
import sys
from pathlib import Path

# Allow running from repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from analytics.schema import validate_game_data, get_schema_errors
from analytics.summary_stats import compute_summary_stats


def find_data_path(cli_path: str | None) -> Path:
    """Resolve path to game data: CLI arg, then data/game_data.json, then sample."""
    if cli_path and os.path.isfile(cli_path):
        return Path(cli_path)
    default = REPO_ROOT / "data" / "game_data.json"
    if default.is_file():
        return default
    sample = REPO_ROOT / "analytics" / "fixtures" / "game_data_sample.json"
    if sample.is_file():
        return sample
    raise FileNotFoundError(
        "No game data found. Provide path to game_data.json or use sample: "
        "analytics/fixtures/game_data_sample.json"
    )


def main() -> None:
    data_path = find_data_path(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"Loading: {data_path}\n")

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    errors = get_schema_errors(data)
    if errors:
        print("Schema validation issues:")
        for e in errors:
            print(f"  - {e}")
        print()
    else:
        print("Schema validation: OK\n")

    stats = compute_summary_stats(data)
    print("--- Summary statistics ---")
    print(f"  Games played:           {stats['games_played']}")
    print(f"  Total playtime:         {stats['total_playtime_minutes']} min")
    print(f"  Best streak:           {stats['best_streak']}")
    print(f"  Unlocked cars:         {stats['unlocked_cars_count']}/4")
    print(f"  Achievements:          {stats['achievements_unlocked']}/9 ({stats['achievement_completion_pct']}%)")
    print(f"  High scores stored:    {stats['high_scores_count']}")
    print(f"  Top score:             {stats['top_score']}")
    if stats["high_scores_count"]:
        print(f"  Mean of stored scores: {stats['score_mean']}")
    print(f"  Best per difficulty:   {stats['best_scores_per_difficulty']}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
