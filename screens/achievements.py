"""
Achievements Screen
SpeedyHighway v1.2.0

"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from game.config import (
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    BLACK, WHITE, GREEN, RED, YELLOW
)


def draw_panel(surface, width, height, x, y, alpha=160, border_color=(64, 64, 64)):
    panel = pygame.Surface((width, height))
    panel.set_alpha(alpha)
    panel.fill(BLACK)
    pygame.draw.rect(panel, border_color, (0, 0, width, height), 3)
    surface.blit(panel, (x, y))


def display_achievements(surface, game_state):
    surface.fill(BLACK)
    
    # Background
    if hasattr(game_state, 'menu_bg_icon_faded') and game_state.menu_bg_icon_faded:
        icon_rect = game_state.menu_bg_icon_faded.get_rect()
        x = (DISPLAY_WIDTH - icon_rect.width) // 2
        y = (DISPLAY_HEIGHT - icon_rect.height) // 2
        surface.blit(game_state.menu_bg_icon_faded, (x, y))
    
    # Fonts
    font_title = pygame.font.SysFont("comicsansms", 48, True)
    font_text = pygame.font.SysFont("lucidaconsole", 16)
    font_small = pygame.font.SysFont("lucidaconsole", 14)
    
    if game_state.reset_confirmation_active:
        _display_reset_confirmation(surface, font_title, font_text, font_small)
    else:
        _display_achievements_list(surface, game_state, font_title, font_text, font_small)


def _display_reset_confirmation(surface, font_title, font_text, font_small):
    panel_width, panel_height = 600, 400
    panel_x = (DISPLAY_WIDTH - panel_width) // 2
    panel_y = (DISPLAY_HEIGHT - panel_height) // 2
    draw_panel(surface, panel_width, panel_height, panel_x, panel_y, 
               alpha=200, border_color=(128, 128, 128))
    
    # Title
    title = font_title.render("RESET PROGRESS", True, RED)
    surface.blit(title, (400 - title.get_width() // 2, panel_y + 30))
    
    warning_text = font_title.render("WARNING!", True, RED)
    surface.blit(warning_text, (400 - warning_text.get_width() // 2, panel_y + 90))
    
    # Warning lines
    confirm_lines = [
        "This will permanently delete ALL your progress:",
        "- All achievements",
        "- High scores", 
        "- Car unlocks",
        "- Settings",
        "",
        "Are you sure you want to continue?"
    ]
    
    for i, line in enumerate(confirm_lines):
        text = font_text.render(line, True, WHITE)
        surface.blit(text, (400 - text.get_width() // 2, panel_y + 140 + i * 25))
    
    # Options
    yes_text = font_title.render("Y - YES, DELETE EVERYTHING", True, RED)
    surface.blit(yes_text, (400 - yes_text.get_width() // 2, panel_y + 310))
    
    no_text = font_title.render("N - NO, KEEP MY DATA", True, GREEN)
    surface.blit(no_text, (400 - no_text.get_width() // 2, panel_y + 350))


def _display_achievements_list(surface, game_state, font_title, font_text, font_small):
    panel_width, panel_height = 700, 450
    panel_x = (DISPLAY_WIDTH - panel_width) // 2
    panel_y = (DISPLAY_HEIGHT - panel_height) // 2
    draw_panel(surface, panel_width, panel_height, panel_x, panel_y)
    
    # Title
    title = font_title.render("ACHIEVEMENTS", True, GREEN)
    surface.blit(title, (400 - title.get_width() // 2, panel_y + 30))
    
    # Achievements list
    for i, achievement in enumerate(game_state.achievements):
        color = GREEN if achievement.unlocked else RED
        status = "[UNLOCKED]" if achievement.unlocked else "[LOCKED]"
        text = f"{status} {achievement.name}: {achievement.description}"
        rendered_text = font_text.render(text, True, color)
        surface.blit(rendered_text, (panel_x + 20, panel_y + 100 + i * 30))
    
    # Instructions
    instructions = [
        "ESC - Back to Menu",
        "R - Reset Progress (WARNING: This will delete all your data!)"
    ]
    
    for i, instruction in enumerate(instructions):
        color = YELLOW if i == 0 else RED
        text = font_small.render(instruction, True, color)
        surface.blit(text, (panel_x + 20, panel_y + 400 + i * 20))
