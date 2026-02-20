# SpeedyHighway – Data Analysis Guide

This document describes the game data model and how to run analytics for player progress, scores, and achievements.

## Data source

- **File**: `data/game_data.json` (created at runtime; not committed to git)
- **Sample data**: `analytics/fixtures/game_data_sample.json` (for testing and demos)

## Data schema (game_data.json)

| Field | Type | Description |
|-------|------|-------------|
| `high_scores` | array | Top 10 entries; each has `score`, `difficulty`, `survival_time`, `date` |
| `difficulty` | int | Current difficulty index (0=Easy, 1=Normal, 2=Hard, 3=Insane) |
| `selected_car` | int | Index of selected car (0–3) |
| `unlocked_cars` | array | List of unlocked car indices |
| `achievements` | object | Achievement id → boolean (unlocked or not) |
| `games_played` | int | Total number of games completed |
| `total_playtime` | int | Cumulative survival time in frames (≈60 per second) |
| `best_streak` | int | Best consecutive games streak |
| `last_daily_challenge` | string \| null | Date of last daily challenge (YYYY-MM-DD) |
| `daily_challenge` | object | Current daily challenge (type, target, description, completed) |
| `highest_difficulty_reached` | int | Highest difficulty index ever played |
| `best_scores_per_difficulty` | array | Best score per difficulty [Easy, Normal, Hard, Insane] (4 elements) |

### High score entry

Each element in `high_scores`:

- `score` (number): Final score
- `difficulty` (string): "Easy" | "Normal" | "Hard" | "Insane"
- `survival_time` (number): Survival time in minutes
- `date` (string): Timestamp, e.g. `"YYYY-MM-DD HH:MM"`

## Analytics module

Location: `analytics/`

- **schema.py**: Validates `game_data` structure and types (including high_scores entry fields: difficulty, survival_time, date). Exports `DIFFICULTY_NAMES`.
- **summary_stats.py**: Computes summary statistics (games played, playtime, achievements, score stats including mean, median, std, min, best per difficulty).
- **exploratory.py**: CSV export and optional plotting: `export_high_scores_csv`, `export_summary_csv`, `run_validation`, `try_plot_score_distribution` (requires matplotlib).

### Usage in code

```python
from analytics import (
    validate_game_data,
    get_schema_errors,
    compute_summary_stats,
    export_high_scores_csv,
    export_summary_csv,
    try_plot_score_distribution,
)

data = {...}  # loaded from game_data.json

if not validate_game_data(data):
    for err in get_schema_errors(data):
        print(err)

stats = compute_summary_stats(data)
# stats["games_played"], stats["top_score"], stats["score_median"], stats["score_std"], etc.

export_high_scores_csv(data, "high_scores.csv")
export_summary_csv(stats, "summary_stats.csv")
try_plot_score_distribution(data, "score_distribution.png")  # if matplotlib installed
```

## Analysis script

**Script**: `scripts/analyze_game_data.py`

- Loads `data/game_data.json` if present, otherwise the sample fixture.
- Validates schema and prints any errors.
- Prints summary statistics (games played, playtime, achievements, high scores, mean/median/std/min, best per difficulty).
- Supports CSV export and JSON output for pipelines.

### Run

From the repository root:

```bash
# Use default (data/game_data.json or sample)
python scripts/analyze_game_data.py

# Use a specific file
python scripts/analyze_game_data.py path/to/game_data.json

# Export high_scores to CSV
python scripts/analyze_game_data.py --export csv --output high_scores.csv

# Export summary metrics to CSV
python scripts/analyze_game_data.py --export summary_csv -o summary_stats.csv

# Output stats as JSON (for scripting)
python scripts/analyze_game_data.py --format json

# Save score distribution plot (requires matplotlib)
python scripts/analyze_game_data.py --plot score_distribution.png

# Quiet mode: only export or JSON
python scripts/analyze_game_data.py --export csv -o out.csv --quiet
```

No extra dependencies for basic use (schema, summary stats, CSV export). For `--plot`, install matplotlib.

## Example metrics

- **Engagement**: `games_played`, `total_playtime`, `best_streak`
- **Skill / progression**: `top_score`, `best_scores_per_difficulty`, `highest_difficulty_reached`
- **Completion**: `achievements_unlocked` / 9, `unlocked_cars` count
- **Score distribution**: `score_mean`, `score_median`, `score_std`, `score_min` from stored high_scores; breakdown by difficulty via `scores_by_difficulty`

## Optional: deeper analysis

For custom histograms, time series, or notebooks:

1. Load `game_data.json` (or the sample) with Python.
2. Use `compute_summary_stats(data)` for standard metrics and `export_high_scores_csv` / `export_summary_csv` for CSV (stdlib only).
3. Use `try_plot_score_distribution(data, path)` or **pandas** and **matplotlib** for score distributions, playtime over time, or achievement unlock order.

The schema and summary stats are designed so that any script or notebook can reuse the same definitions and stay consistent with the game’s data format.
