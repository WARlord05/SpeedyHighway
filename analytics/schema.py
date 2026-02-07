"""
Game data schema and validation for SpeedyHighway.
Defines the expected structure of game_data.json and validates loaded data.
"""

from typing import Any


# Expected top-level keys and their value types
GAME_DATA_SCHEMA = {
    "high_scores": list,
    "difficulty": int,
    "selected_car": int,
    "unlocked_cars": list,
    "achievements": dict,
    "games_played": int,
    "total_playtime": int,
    "best_streak": int,
    "last_daily_challenge": (type(None), str),
    "daily_challenge": dict,
    "highest_difficulty_reached": int,
    "best_scores_per_difficulty": list,
}

# High score entry schema (each item in high_scores)
HIGH_SCORE_ENTRY_KEYS = {"score", "difficulty", "survival_time", "date"}


def _check_type(value: Any, expected: type | tuple) -> bool:
    """Return True if value matches expected type(s)."""
    if isinstance(expected, tuple):
        return any(isinstance(value, t) for t in expected)
    return isinstance(value, expected)


def get_schema_errors(data: dict) -> list[str]:
    """
    Validate game_data against the schema. Returns a list of error messages.
    Empty list means valid.
    """
    errors = []
    if not isinstance(data, dict):
        return ["game_data must be a dict"]

    for key, expected_type in GAME_DATA_SCHEMA.items():
        if key not in data:
            errors.append(f"Missing required key: '{key}'")
            continue
        val = data[key]
        if not _check_type(val, expected_type):
            errors.append(
                f"'{key}' must be {expected_type!r}, got {type(val).__name__}"
            )

    # Validate high_scores entries
    high_scores = data.get("high_scores", [])
    if isinstance(high_scores, list):
        for i, entry in enumerate(high_scores):
            if not isinstance(entry, dict):
                errors.append(f"high_scores[{i}] must be a dict")
                continue
            missing = HIGH_SCORE_ENTRY_KEYS - set(entry.keys())
            if missing:
                errors.append(
                    f"high_scores[{i}] missing keys: {sorted(missing)}"
                )
            if "score" in entry and not isinstance(entry["score"], (int, float)):
                errors.append(f"high_scores[{i}].score must be numeric")

    # Validate list lengths where fixed
    best_scores = data.get("best_scores_per_difficulty", [])
    if isinstance(best_scores, list) and len(best_scores) != 4:
        errors.append(
            "best_scores_per_difficulty must have exactly 4 elements"
        )

    return errors


def validate_game_data(data: dict) -> bool:
    """
    Return True if game_data is valid according to the schema, False otherwise.
    """
    return len(get_schema_errors(data)) == 0
