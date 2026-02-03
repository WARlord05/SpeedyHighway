"""
Game configuration
SpeedyHighway v1.2.0
"""

__version__ = "1.2.0"
__author__ = "Tanay Vidhate (WARlord05)"
__description__ = "Speedy Highway Racing Game - Enhanced Edition"

# Display And Color Settings
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Difficulty settings
DIFFICULTY_MODES = ["Easy", "Normal", "Hard", "Insane"]
DIFFICULTY_MULTIPLIERS = [0.7, 1.0, 1.3, 1.6]
SCORE_MULTIPLIERS = [1.0, 1.2, 1.5, 2.0]

# Road and lanes
LANE_POSITIONS = [215, 295, 415, 495]
ROAD_MIN_X = 200
ROAD_MAX_X = 520

# Cars and player and enemy car configuration and Settings
AVAILABLE_CARS = ["car.png", "car_blue.png", "car_red.png", "special"]
CAR_NAMES = ["Default", "Lamborghini", "Ferrari", "Rolls Royce"]
CAR_UNLOCK_SCORES = [0, 500, 1500, 3000]

CAR_WIDTH = 99
CAR_START_X = 215

ENEMY_CAR_WIDTH = 99
ENEMY_CAR_HEIGHT = 100
ENEMY_START_Y = -600
BASE_ENEMY_SPEED = 5
BASE_BG_SPEED = 3

# Speed limits per difficulty [Easy, Normal, Hard, Insane]
MAX_ENEMY_SPEEDS = [10, 15, 18, None] 
MAX_BG_SPEEDS = [7, 12, 15, None]

# Animation
SPECIAL_CAR_FRAMES = 12
SPECIAL_CAR_ANIMATION_SPEED = 15

# Input
KEY_REPEAT_DELAY = 11

# Sound files
SOUND_FILES = {
    'crash': 'crash.wav',
    'off_road': 'off_road.wav',
    'engine_default': 'engine_default.wav',
    'engine_default_loop': 'engine_default1.wav',
    'engine_blue': 'engine_blue.wav',
    'engine_blue_loop': 'engine_blue1.wav',
    'engine_red': 'engine_red.wav',
    'engine_red_loop': 'engine_red1.wav',
    'engine_special': 'engine_special.wav',
    'engine_special_loop': 'engine_special1.wav',
    'near_miss': 'near_miss.wav',
    'achievement': 'achievement.wav',
    'menu_select': 'menu_select.wav',
    'car_unlock': 'car_unlock.wav'
}

MUSIC_FILES = {
    'menu_music': 'menu_music.mp3',
    'game_music': 'game_music.mp3'
}

# Daily challenges
DAILY_CHALLENGES = [
    {"type": "score", "target": 2000, "description": "Score 2000 points"},
    {"type": "survival", "target": 3600, "description": "Survive for 1 minute"},
    {"type": "near_miss", "target": 15, "description": "Get 15 near misses"},
    {"type": "lane_change", "target": 30, "description": "Change lanes 30 times"}
]

# Default game data structure
DEFAULT_GAME_DATA = {
    "high_scores": [],
    "difficulty": 1,
    "selected_car": 0,
    "unlocked_cars": [0],
    "achievements": {},
    "games_played": 0,
    "total_playtime": 0,
    "best_streak": 0,
    "last_daily_challenge": None,
    "daily_challenge": {},
    "highest_difficulty_reached": 0,
    "best_scores_per_difficulty": [0, 0, 0, 0]
}
