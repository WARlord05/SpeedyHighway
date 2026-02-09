#!/usr/bin/env python3
"""
SpeedyHighway Game Data Analysis Script.
Loads game_data.json (or sample fixture), validates schema, and prints summary stats.
Supports CSV export and optional JSON output for downstream analytics.

Run from repo root:
  python scripts/analyze_game_data.py [path_to_game_data.json]
  python scripts/analyze_game_data.py --export csv --output high_scores.csv
  python scripts/analyze_game_data.py --format json
  python scripts/analyze_game_data.py --plot score_distribution.png
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Allow running from repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from analytics.schema import get_schema_errors, validate_game_data
from analytics.summary_stats import compute_summary_stats
from analytics.exploratory import (
    export_high_scores_csv,
    export_summary_csv,
    try_plot_score_distribution,
)


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
    parser = argparse.ArgumentParser(
        description="Analyze SpeedyHighway game_data.json: validate schema and print/export stats."
    )
    parser.add_argument(
        "data_path",
        nargs="?",
        default=None,
        help="Path to game_data.json (default: data/game_data.json or sample fixture)",
    )
    parser.add_argument(
        "--export",
        choices=("csv", "summary_csv"),
        default=None,
        help="Export high_scores to CSV, or summary metrics to CSV",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output path for --export or --plot (default: high_scores.csv / summary_stats.csv)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format for summary stats (default: text)",
    )
    parser.add_argument(
        "--plot",
        metavar="PATH",
        default=None,
        help="Save score distribution plot to PATH (requires matplotlib)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress normal summary output (useful with --export/--format json only)",
    )
    args = parser.parse_args()

    data_path = find_data_path(args.data_path)
    if not args.quiet:
        print(f"Loading: {data_path}\n")

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    errors = get_schema_errors(data)
    if errors:
        if not args.quiet:
            print("Schema validation issues:")
            for e in errors:
                print(f"  - {e}")
            print()
    else:
        if not args.quiet:
            print("Schema validation: OK\n")

    stats = compute_summary_stats(data)

    if args.export == "csv":
        out = args.output or (REPO_ROOT / "high_scores.csv")
        export_high_scores_csv(data, out)
        print(f"Exported high_scores to {out}")
    elif args.export == "summary_csv":
        out = args.output or (REPO_ROOT / "summary_stats.csv")
        export_summary_csv(stats, out)
        print(f"Exported summary stats to {out}")

    if args.plot:
        if try_plot_score_distribution(data, args.plot):
            print(f"Saved score distribution plot to {args.plot}")
        else:
            print("Plot skipped (install matplotlib and ensure high_scores exist)", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(stats, indent=2))
    elif not args.quiet:
        print("--- Summary statistics ---")
        print(f"  Games played:           {stats['games_played']}")
        print(f"  Total playtime:         {stats['total_playtime_minutes']} min")
        print(f"  Best streak:            {stats['best_streak']}")
        print(f"  Unlocked cars:          {stats['unlocked_cars_count']}/4")
        print(
            f"  Achievements:           {stats['achievements_unlocked']}/9 "
            f"({stats['achievement_completion_pct']}%)"
        )
        print(f"  High scores stored:     {stats['high_scores_count']}")
        print(f"  Top score:              {stats['top_score']}")
        if stats["high_scores_count"]:
            print(f"  Mean of stored scores:  {stats['score_mean']}")
            print(f"  Median of stored scores: {stats['score_median']}")
            print(f"  Std dev of stored scores: {stats['score_std']}")
            print(f"  Min stored score:       {stats['score_min']}")
        print(f"  Best per difficulty:    {stats['best_scores_per_difficulty']}")
        print()
        print("Done.")


if __name__ == "__main__":
    main()
