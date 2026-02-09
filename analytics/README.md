# Analytics

Data schema validation, summary statistics, and export utilities for SpeedyHighway game data.

- **schema.py** – Validate `game_data.json` structure (including high_scores entry types and difficulty values). Exports `DIFFICULTY_NAMES`.
- **summary_stats.py** – Compute games played, playtime, achievements, score stats (mean, median, std, min, best per difficulty).
- **exploratory.py** – CSV export (`export_high_scores_csv`, `export_summary_csv`), `run_validation`, and optional `try_plot_score_distribution` (matplotlib).
- **fixtures/game_data_sample.json** – Sample data for testing and analysis.

See **docs/DATA_ANALYSIS.md** for the full data dictionary, script options (`--export`, `--format`, `--plot`), and usage examples.
