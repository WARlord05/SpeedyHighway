"""
Car Selection Screen
SpeedyHighway v1.2.0

"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from game.config import (
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    BLACK, WHITE, BLUE, YELLOW,
    CAR_NAMES
)


def draw_panel(surface, width, height, x, y, alpha=160):
    panel = pygame.Surface((width, height))
    panel.set_alpha(alpha)
    panel.fill(BLACK)
    pygame.draw.rect(panel, (64, 64, 64), (0, 0, width, height), 3)
    surface.blit(panel, (x, y))


def display_car_selection(surface, game_state):
    surface.fill(BLACK)
    
    # Background
    if hasattr(game_state, 'menu_bg_icon_faded') and game_state.menu_bg_icon_faded:
        icon_rect = game_state.menu_bg_icon_faded.get_rect()
        x = (DISPLAY_WIDTH - icon_rect.width) // 2
        y = (DISPLAY_HEIGHT - icon_rect.height) // 2
        surface.blit(game_state.menu_bg_icon_faded, (x, y))
    
    # Panel
    panel_width, panel_height = 600, 450
    panel_x = (DISPLAY_WIDTH - panel_width) // 2
    panel_y = (DISPLAY_HEIGHT - panel_height) // 2
    draw_panel(surface, panel_width, panel_height, panel_x, panel_y)
    
    # Fonts
    font_title = pygame.font.SysFont("comicsansms", 48, True)
    font_text = pygame.font.SysFont("lucidaconsole", 20)
    
    # Title
    title = font_title.render("CAR SELECTION", True, BLUE)
    surface.blit(title, (400 - title.get_width() // 2, panel_y + 30))
    
    # Car preview
    preview_y = panel_y + 80
    surface.blit(game_state.carImg, (400 - game_state.carImg.get_width() // 2, preview_y))
    
    # Car list
    unlocked_cars = game_state.game_data["unlocked_cars"]
    
    for i, car_index in enumerate(unlocked_cars):
        color = YELLOW if car_index == game_state.current_car else WHITE
        car_text = f"{CAR_NAMES[car_index]}"
        if car_index == game_state.current_car:
            car_text = f"> {car_text} <"
        
        text = font_text.render(car_text, True, color)
        surface.blit(text, (400 - text.get_width() // 2, panel_y + 200 + i * 40))
    
    # Instructions
    instructions = [
        "A/D or LEFT/RIGHT - Navigate",
        "SPACE - Select Car",
        "ESC - Back to Menu"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font_text.render(instruction, True, WHITE)
        surface.blit(text, (400 - text.get_width() // 2, panel_y + 360 + i * 25))
