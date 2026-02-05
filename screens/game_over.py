"""
Game Over Screen
SpeedyHighway v1.2.0

"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from game.config import (
    BLACK, WHITE, RED, YELLOW,
    DIFFICULTY_MODES
)


def display_game_over_screen(surface, game_state):
    surface.fill(BLACK)
    
    # Fonts
    font_title = pygame.font.SysFont("comicsansms", 72, True)
    font_text = pygame.font.SysFont("lucidaconsole", 20)
    font_small = pygame.font.SysFont("lucidaconsole", 16)
    
    # Title
    title = font_title.render("GAME OVER", True, RED)
    surface.blit(title, (400 - title.get_width() // 2, 100))
    
    # Stats
    stats = [
        f"Final Score: {game_state.total_score}",
        f"Base Score: {game_state.base_score}",
        f"Bonus Score: {game_state.bonus_score}",
        f"Near Misses: {game_state.near_miss_count}",
        f"Lane Changes: {game_state.lane_change_count}",
        f"Survival Time: {game_state.survival_time // 60}s",
        f"Difficulty: {DIFFICULTY_MODES[game_state.current_difficulty]}"
    ]
    
    for i, stat in enumerate(stats):
        text = font_text.render(stat, True, WHITE)
        surface.blit(text, (400 - text.get_width() // 2, 200 + i * 30))
    
    # Instruction
    instruction = font_small.render("Press SPACE to return to menu", True, YELLOW)
    surface.blit(instruction, (400 - instruction.get_width() // 2, 500))
