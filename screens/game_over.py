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

    screen_w = surface.get_width()
    center_x = screen_w // 2

    # Fonts (gamified but safe)
    font_title = pygame.font.SysFont("impact", 80)
    font_text = pygame.font.SysFont("consolas", 32, True)
    font_small = pygame.font.SysFont("consolas", 24)

    # Title
        # Title
    title = font_title.render("G  A  M  E  O  V  E  R", True, RED)
    title_y = 100
    surface.blit(title, (center_x - title.get_width() // 2, title_y))

    # Divider line (place BELOW title, not through it)
    line_y = title_y + title.get_height() + 10
    line_width = title.get_width() + 40
    pygame.draw.line(
        surface,
        WHITE,
        (center_x - line_width // 2, line_y),
        (center_x + line_width // 2, line_y),
        2
    )


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

    start_y = 220
    for i, stat in enumerate(stats):
        text = font_text.render(stat, True, WHITE)
        surface.blit(text, (center_x - text.get_width() // 2, start_y + i * 36))

    # Instruction
    instruction = font_small.render("Press SPACE to return to menu", True, YELLOW)
    surface.blit(instruction, (center_x - instruction.get_width() // 2, 520))
