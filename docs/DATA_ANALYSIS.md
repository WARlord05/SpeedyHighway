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

- **schema.py**: Validates `game_data` structure and types.
- **summary_stats.py**: Computes summary statistics (games played, playtime, achievements, score stats, best per difficulty).

### Usage in code

```python
from analytics import validate_game_data, get_schema_errors, compute_summary_stats

data = {...}  # loaded from game_data.json

if not validate_game_data(data):
    for err in get_schema_errors(data):
        print(err)

stats = compute_summary_stats(data)
# stats["games_played"], stats["top_score"], stats["achievement_completion_pct"], etc.
```

## Analysis script

**Script**: `scripts/analyze_game_data.py`

- Loads `data/game_data.json` if present, otherwise the sample fixture.
- Validates schema and prints any errors.
- Prints summary statistics (games played, playtime, achievements, high scores, best per difficulty).

### Run

From the repository root:

```bash
# Use default (data/game_data.json or sample)
python scripts/analyze_game_data.py

# Use a specific file
python scripts/analyze_game_data.py path/to/game_data.json
```

No extra dependencies beyond the project’s `requirements.txt` (pygame is not required for this script; only the `analytics` package and standard library are used).

## Example metrics

- **Engagement**: `games_played`, `total_playtime`, `best_streak`
- **Skill / progression**: `top_score`, `best_scores_per_difficulty`, `highest_difficulty_reached`
- **Completion**: `achievements_unlocked` / 9, `unlocked_cars` count
- **Score distribution**: From `high_scores` you can compute mean, median, and breakdown by difficulty

## Optional: deeper analysis

For histograms, time series, or exports (e.g. CSV), you can:

1. Load `game_data.json` (or the sample) with Python.
2. Use `analytics.summary_stats.compute_summary_stats(data)` for standard metrics.
3. Optionally use **pandas** and **matplotlib** (add to `requirements.txt` and install) to plot score distributions, playtime over time, or achievement unlock order.

The schema and summary stats are designed so that any script or notebook can reuse the same definitions and stay consistent with the game’s data format.
