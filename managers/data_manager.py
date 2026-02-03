"""
Data Manager Module
SpeedyHighway v1.2.0
"""

import os
import sys
import json
# Add parent directory to path for cross-package imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game.utils import get_resource_path
from game.config import DEFAULT_GAME_DATA


def load_game_data():
    try:
        data_path = get_resource_path(os.path.join("data", "game_data.json"))
        with open(data_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return create_default_game_data()


def create_default_game_data():
    return DEFAULT_GAME_DATA.copy()


def save_game_data(game_data):
    if game_data is None:
        game_data = create_default_game_data()
    
    try:
        data_path = get_resource_path(os.path.join("data", "game_data.json"))
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        with open(data_path, "w") as f:
            json.dump(game_data, f, indent=2)
    except (OSError, PermissionError):
        try:
            if hasattr(sys, '_MEIPASS'):
                data_path = os.path.join(os.path.dirname(sys.executable), "game_data.json")
            else:
                data_path = os.path.join(os.getcwd(), "game_data.json")
            with open(data_path, "w") as f:
                json.dump(game_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save game data: {e}")


def ensure_game_data_exists(game_data):
    if game_data is None:
        return load_game_data()
    
    try:
        data_path = get_resource_path(os.path.join("data", "game_data.json"))
        if not os.path.exists(data_path):
            save_game_data(game_data)
    except Exception:
        pass
    
    return game_data
