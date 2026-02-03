"""
High Scores Screen
SpeedyHighway v1.2.0

Handles high scores display.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from game.config import (
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    BLACK, WHITE, GREEN, YELLOW,
    DIFFICULTY_MODES
)


def draw_panel(surface, width, height, x, y, alpha=160):
    panel = pygame.Surface((width, height))
    panel.set_alpha(alpha)
    panel.fill(BLACK)
    pygame.draw.rect(panel, (64, 64, 64), (0, 0, width, height), 3)
    surface.blit(panel, (x, y))


def display_high_scores(surface, game_state):
    surface.fill(BLACK)
    
    # Background
    if hasattr(game_state, 'menu_bg_icon_faded') and game_state.menu_bg_icon_faded:
        icon_rect = game_state.menu_bg_icon_faded.get_rect()
        x = (DISPLAY_WIDTH - icon_rect.width) // 2
        y = (DISPLAY_HEIGHT - icon_rect.height) // 2
        surface.blit(game_state.menu_bg_icon_faded, (x, y))
    
    # Panel
    panel_width, panel_height = 700, 450
    panel_x = (DISPLAY_WIDTH - panel_width) // 2
    panel_y = (DISPLAY_HEIGHT - panel_height) // 2
    draw_panel(surface, panel_width, panel_height, panel_x, panel_y)
    
    # Fonts
    font_title = pygame.font.SysFont("comicsansms", 48, True)
    font_text = pygame.font.SysFont("lucidaconsole", 18)
    font_highlight = pygame.font.SysFont("comicsansms", 32, True)
    
    # Title
    title = font_title.render("HIGH SCORES", True, YELLOW)
    surface.blit(title, (400 - title.get_width() // 2, panel_y + 30))
    
    # Best score highlight
    highest_difficulty = game_state.game_data.get("highest_difficulty_reached", 0)
    best_scores = game_state.game_data.get("best_scores_per_difficulty", [0, 0, 0, 0])
    best_score_in_highest_diff = best_scores[highest_difficulty]
    
    if best_score_in_highest_diff > 0:
        highlight_text = f"Your Best in {DIFFICULTY_MODES[highest_difficulty]}: {best_score_in_highest_diff}"
        highlight_render = font_highlight.render(highlight_text, True, GREEN)
        surface.blit(highlight_render, (400 - highlight_render.get_width() // 2, panel_y + 80))
    
    # High scores list
    high_scores = game_state.game_data.get("high_scores", [])
    start_y = panel_y + 130 if best_score_in_highest_diff > 0 else panel_y + 100
    
    for i, score_data in enumerate(high_scores[:10]):
        score_text = f"{i+1}. {score_data['score']} - {score_data['difficulty']} - {score_data['date']}"
        text = font_text.render(score_text, True, WHITE)
        surface.blit(text, (panel_x + 20, start_y + i * 30))
    
    # Instruction
    instruction = font_text.render("Press ESC to return to menu", True, YELLOW)
    surface.blit(instruction, (400 - instruction.get_width() // 2, panel_y + 410))
