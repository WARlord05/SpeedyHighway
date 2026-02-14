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


def draw_panel(surface, width, height, x, y, alpha=200):
    panel = pygame.Surface((width, height))
    panel.set_alpha(alpha)
    panel.fill(BLACK)
    pygame.draw.rect(panel, (64, 64, 64), (0, 0, width, height), 3)
    surface.blit(panel, (x, y))


def display_car_selection(surface, game_state):
    surface.fill(BLACK)

    center_x = DISPLAY_WIDTH // 2
    center_y = DISPLAY_HEIGHT // 2

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

    # Fonts (consistent with menu & game over)
    font_title = pygame.font.SysFont("impact", 60)
    font_car = pygame.font.SysFont("bahnschrift", 32, True)
    font_selected = pygame.font.SysFont("bahnschrift", 36, True)
    font_instructions = pygame.font.SysFont("bahnschrift", 22)

    # Title
    title = font_title.render("CAR SELECTION", True, YELLOW)
    surface.blit(title, (center_x - title.get_width() // 2, panel_y + 30))

    # Car preview
    preview_y = panel_y + 90
    surface.blit(
        game_state.carImg,
        (center_x - game_state.carImg.get_width() // 2, preview_y)
    )

    # Car list
    unlocked_cars = game_state.game_data["unlocked_cars"]

    for i, car_index in enumerate(unlocked_cars):
        car_name = CAR_NAMES[car_index]

        if car_index == game_state.current_car:
            color = YELLOW
            text = font_selected.render(f"> {car_name} <", True, color)
        else:
            color = WHITE
            text = font_car.render(car_name, True, color)

        surface.blit(
            text,
            (center_x - text.get_width() // 2, panel_y + 210 + i * 40)
        )

    # Instructions
    instructions = [
        "A/D or LEFT/RIGHT - Navigate",
        "SPACE - Select Car",
        "ESC - Back to Menu"
    ]

    for i, instruction in enumerate(instructions):
        text = font_instructions.render(instruction, True, WHITE)
        surface.blit(
            text,
            (center_x - text.get_width() // 2, panel_y + 360 + i * 25)
        )
