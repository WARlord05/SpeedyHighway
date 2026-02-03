"""
Achievement Manager Module
SpeedyHighway v1.2.0

Handles achievements
"""

import os
import sys
import random
import hashlib
from datetime import datetime

# Add parent directory to path for cross-package imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.config import DAILY_CHALLENGES


class Achievement:
    ## Represents achievement.
    def __init__(self, id, name, description, condition):
        self.id = id
        self.name = name
        self.description = description
        self.condition = condition
        self.unlocked = False


def create_achievements(game_instance):
    return [
        Achievement("first_game", "First Drive", "Play your first game", 
                   lambda: game_instance.games_played >= 1),
        Achievement("score_1000", "Road Warrior", "Score 1000 points", 
                   lambda: game_instance.total_score >= 1000),
        Achievement("score_5000", "Highway Legend", "Score 5000 points", 
                   lambda: game_instance.total_score >= 5000 and game_instance.current_difficulty >= 1),
        Achievement("near_miss_10", "Close Call", "Get 10 near misses in one game", 
                   lambda: game_instance.near_miss_count >= 10),
        Achievement("lane_master", "Lane Master", "Change lanes 50 times in one game", 
                   lambda: game_instance.lane_change_count >= 50),
        Achievement("survivor", "Survivor", "Survive for 2 minutes", 
                   lambda: game_instance.survival_time >= 7200),
        Achievement("speed_demon", "Speed Demon", "Reach maximum speed", 
                   lambda: game_instance.check_speed_demon_achievement()),
        Achievement("speed_god", "Speed God", "Reach 40 speed in Insane difficulty", 
                   lambda: game_instance.check_speed_god_achievement()),
        Achievement("perfect_game", "Perfect Game", "Complete daily challenge", 
                   lambda: game_instance.daily_challenge.get("completed", False))
    ]


def load_achievement_states(achievements, game_data):
    for achievement in achievements:
        achievement.unlocked = game_data.get("achievements", {}).get(achievement.id, False)


def check_achievements(achievements, game_data, sound_manager):
    achievements_changed = False
    
    for achievement in achievements:
        if not achievement.unlocked and achievement.condition():
            achievement.unlocked = True
            game_data["achievements"][achievement.id] = True
            print(f"Achievement Unlocked: {achievement.name} - {achievement.description}")
            sound_manager.play_sound('achievement')
            achievements_changed = True
    
    return achievements_changed


def generate_daily_challenge(game_data):
    today = datetime.now().strftime("%Y-%m-%d")
    
    if game_data.get("last_daily_challenge") != today:
        challenge_seed = int(hashlib.md5(today.encode()).hexdigest()[:8], 16)
        challenge_random = random.Random(challenge_seed)
        challenge = challenge_random.choice(DAILY_CHALLENGES).copy()
        challenge["completed"] = False
        game_data["last_daily_challenge"] = today
        game_data["daily_challenge"] = challenge
        return challenge, True  
    return game_data.get("daily_challenge", {}), False
