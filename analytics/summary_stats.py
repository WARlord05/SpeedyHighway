"""
Summary statistics and metrics from SpeedyHighway game data.
"""

from typing import Any


def compute_summary_stats(data: dict) -> dict[str, Any]:
    """
    Compute summary statistics from game_data. Safe to call with partial data;
    missing keys are treated as default/zero.
    """
    high_scores = data.get("high_scores") or []
    achievements = data.get("achievements") or {}
    best_per_diff = data.get("best_scores_per_difficulty") or [0, 0, 0, 0]
    difficulty_names = ["Easy", "Normal", "Hard", "Insane"]

    # Score distribution from high_scores
    scores = [e["score"] for e in high_scores if isinstance(e, dict) and "score" in e]
    by_difficulty = {}
    for e in high_scores:
        if not isinstance(e, dict) or "difficulty" not in e:
            continue
        d = e["difficulty"]
        by_difficulty[d] = by_difficulty.get(d, []) + [e.get("score", 0)]

    return {
        "games_played": data.get("games_played", 0),
        "total_playtime_frames": data.get("total_playtime", 0),
        "total_playtime_minutes": round((data.get("total_playtime", 0) or 0) / 60, 1),
        "best_streak": data.get("best_streak", 0),
        "current_difficulty_index": data.get("difficulty", 1),
        "unlocked_cars_count": len(data.get("unlocked_cars") or [0]),
        "achievements_unlocked": sum(1 for v in achievements.values() if v),
        "achievements_total": 9,
        "achievement_completion_pct": round(100 * sum(1 for v in achievements.values() if v) / 9, 1),
        "high_scores_count": len(scores),
        "top_score": max(scores) if scores else 0,
        "score_mean": round(sum(scores) / len(scores), 1) if scores else 0,
        "scores_by_difficulty": {k: (len(v), max(v) if v else 0) for k, v in by_difficulty.items()},
        "best_scores_per_difficulty": {
            difficulty_names[i]: best_per_diff[i]
            for i in range(min(4, len(best_per_diff)))
        },
        "highest_difficulty_reached_index": data.get("highest_difficulty_reached", 0),
    }
