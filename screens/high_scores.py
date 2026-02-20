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


def draw_panel(surface, width, height, x, y, alpha=180):
    panel = pygame.Surface((width, height))
    panel.set_alpha(alpha)
    panel.fill(BLACK)
    pygame.draw.rect(panel, (64, 64, 64), (0, 0, width, height), 3)
    surface.blit(panel, (x, y))


def display_high_scores(surface, game_state):
    surface.fill(BLACK)
    center_x = DISPLAY_WIDTH // 2

    # Background
    if hasattr(game_state, 'menu_bg_icon_faded') and game_state.menu_bg_icon_faded:
        icon_rect = game_state.menu_bg_icon_faded.get_rect()
        x = (DISPLAY_WIDTH - icon_rect.width) // 2
        y = (DISPLAY_HEIGHT - icon_rect.height) // 2
        surface.blit(game_state.menu_bg_icon_faded, (x, y))

    # Panel
    panel_width, panel_height = 700, 470
    panel_x = (DISPLAY_WIDTH - panel_width) // 2
    panel_y = (DISPLAY_HEIGHT - panel_height) // 2
    draw_panel(surface, panel_width, panel_height, panel_x, panel_y)

    # Fonts (consistent with rest of UI)
    font_title = pygame.font.SysFont("impact", 56)
    font_text = pygame.font.SysFont("bahnschrift", 22)
    font_highlight = pygame.font.SysFont("bahnschrift", 26, True)
    font_instruction = pygame.font.SysFont("bahnschrift", 20)

    # Title
    title = font_title.render("HIGH SCORES", True, YELLOW)
    surface.blit(title, (center_x - title.get_width() // 2, panel_y + 25))

    # Divider
    pygame.draw.line(surface, WHITE,
                     (panel_x + 40, panel_y + 90),
                     (panel_x + panel_width - 40, panel_y + 90), 2)

    # Best score highlight
    highest_difficulty = game_state.game_data.get("highest_difficulty_reached", 0)
    best_scores = game_state.game_data.get("best_scores_per_difficulty", [0, 0, 0, 0])
    best_score_in_highest_diff = best_scores[highest_difficulty]

    list_start_y = panel_y + 110

    if best_score_in_highest_diff > 0:
        highlight_text = f"BEST ({DIFFICULTY_MODES[highest_difficulty]}): {best_score_in_highest_diff}"
        highlight_render = font_highlight.render(highlight_text, True, GREEN)
        surface.blit(highlight_render,
                     (center_x - highlight_render.get_width() // 2, panel_y + 105))
        list_start_y += 40

    # High scores list (center aligned)
    high_scores = game_state.game_data.get("high_scores", [])

    for i, score_data in enumerate(high_scores[:10]):
        score_text = f"{i+1}.  {score_data['score']}   |   {score_data['difficulty']}   |   {score_data['date']}"
        text = font_text.render(score_text, True, WHITE)
        surface.blit(text, (center_x - text.get_width() // 2, list_start_y + i * 30))

    # Bottom divider
    pygame.draw.line(surface, WHITE,
                     (panel_x + 40, panel_y + panel_height - 70),
                     (panel_x + panel_width - 40, panel_y + panel_height - 70), 1)

    # Instruction
    instruction = font_instruction.render("Press ESC to return to menu", True, YELLOW)
    surface.blit(instruction,
                 (center_x - instruction.get_width() // 2, panel_y + panel_height - 50))
