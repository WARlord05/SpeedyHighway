"""
Menu Screen
SpeedyHighway v1.2.0
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from game.config import (
    DISPLAY_WIDTH, DISPLAY_HEIGHT, 
    BLACK, WHITE, GREEN, RED, BLUE, YELLOW,
    DIFFICULTY_MODES, __version__
)


def draw_panel(surface, width, height, x, y, alpha=160, border_color=(120, 120, 120)):
    panel = pygame.Surface((width, height))
    panel.set_alpha(alpha)
    panel.fill(BLACK)
    pygame.draw.rect(panel, border_color, (0, 0, width, height), 3)
    surface.blit(panel, (x, y))


def display_main_menu(surface, game_state):
    center_x = DISPLAY_WIDTH // 2

    # Background
    if hasattr(game_state, 'menu_bg_icon_faded') and game_state.menu_bg_icon_faded:
        icon_rect = game_state.menu_bg_icon_faded.get_rect()
        x = (DISPLAY_WIDTH - icon_rect.width) // 2
        y = (DISPLAY_HEIGHT - icon_rect.height) // 2
        surface.blit(game_state.menu_bg_icon_faded, (x, y))
    
    # Panel
    panel_width, panel_height = 650, 450
    panel_x = (DISPLAY_WIDTH - panel_width) // 2
    panel_y = 60
    draw_panel(surface, panel_width, panel_height, panel_x, panel_y)
    
    # Title
    font_title = pygame.font.SysFont("impact", 60)
    title = font_title.render("SPEEDY HIGHWAY", True, WHITE)
    surface.blit(title, (center_x - title.get_width() // 2, 80))
    
    # Version
    font_version = pygame.font.SysFont("bahnschrift", 18, True)
    version_text = font_version.render(f"v{__version__} - Enhanced Edition", True, YELLOW)
    surface.blit(version_text, (center_x - version_text.get_width() // 2, 145))
    
    # Menu options
    font_menu = pygame.font.SysFont("bahnschrift", 28, True)
    fullscreen_status = "ON" if game_state.fullscreen_mode else "OFF"
    options = [
        "SPACE - Start Game",
        "H - High Scores",
        "A - Achievements", 
        "C - Car Selection",
        f"D - Difficulty: {DIFFICULTY_MODES[game_state.current_difficulty]}",
        f"F - Fullscreen: {fullscreen_status}",
        "ESC - Quit"
    ]
    
    for i, option in enumerate(options):
        if "Start Game" in option:
            color = GREEN
        elif "Quit" in option:
            color = RED
        else:
            color = WHITE

        text = font_menu.render(option, True, color)
        surface.blit(text, (center_x - text.get_width() // 2, 200 + i * 35))
    
    # Volume info
    font_small = pygame.font.SysFont("bahnschrift", 18)
    volume_percent = int(game_state.sound_manager.master_volume * 100)
    volume_text = f"Sound Volume: {volume_percent}% (+/- to adjust, M to mute)"
    volume_render = font_small.render(volume_text, True, YELLOW)
    surface.blit(volume_render, (center_x - volume_render.get_width() // 2, 435))
    
    music_volume_percent = int(game_state.sound_manager.music_volume * 100)
    music_text = f"Music Volume: {music_volume_percent}% ([/] to adjust, N to mute)"
    music_render = font_small.render(music_text, True, YELLOW)
    surface.blit(music_render, (center_x - music_render.get_width() // 2, 455))
    
    fullscreen_text = "ALT+ENTER - Toggle fullscreen anytime"
    fullscreen_render = font_small.render(fullscreen_text, True, GREEN)
    surface.blit(fullscreen_render, (center_x - fullscreen_render.get_width() // 2, 475))

    # Seed info
    seed_text = f"Entropy Seed: {game_state._entropy_seed} (S to set custom seed)"
    seed_render = font_small.render(seed_text, True, BLUE)
    seed_bg = pygame.Surface((seed_render.get_width() + 10, seed_render.get_height() + 4))
    seed_bg.set_alpha(180)
    seed_bg.fill(BLACK)
    surface.blit(seed_bg, (5, 8))
    surface.blit(seed_render, (10, 10))
    
    # Daily challenge
    if game_state.daily_challenge:
        challenge_text = f"Daily Challenge: {game_state.daily_challenge.get('description', 'N/A')}"
        if game_state.daily_challenge.get('completed', False):
            challenge_text += " [COMPLETE]"
        text = font_small.render(challenge_text, True, YELLOW)
        challenge_bg = pygame.Surface((text.get_width() + 10, text.get_height() + 4))
        challenge_bg.set_alpha(180)
        challenge_bg.fill(BLACK)
        surface.blit(challenge_bg, (5, 548))
        surface.blit(text, (10, 550))


def display_seed_input(surface, game_state):
    center_x = DISPLAY_WIDTH // 2

    # Background
    if hasattr(game_state, 'menu_bg_icon_faded') and game_state.menu_bg_icon_faded:
        icon_rect = game_state.menu_bg_icon_faded.get_rect()
        x = (DISPLAY_WIDTH - icon_rect.width) // 2
        y = (DISPLAY_HEIGHT - icon_rect.height) // 2
        surface.blit(game_state.menu_bg_icon_faded, (x, y))
    
    # Panel
    panel_width, panel_height = 550, 400
    panel_x = (DISPLAY_WIDTH - panel_width) // 2
    panel_y = (DISPLAY_HEIGHT - panel_height) // 2
    draw_panel(surface, panel_width, panel_height, panel_x, panel_y, alpha=180)
    
    # Fonts (consistent typography)
    font_title = pygame.font.SysFont("impact", 48)
    font_text = pygame.font.SysFont("bahnschrift", 24, True)
    font_small = pygame.font.SysFont("bahnschrift", 18)
    
    # Title
    title = font_title.render("CUSTOM ENTROPY SEED", True, YELLOW)
    surface.blit(title, (center_x - title.get_width() // 2, 150))
    
    # Instruction
    instruction = font_text.render("Enter a custom seed (integer):", True, WHITE)
    surface.blit(instruction, (center_x - instruction.get_width() // 2, 250))
    
    # Input box
    input_box_rect = pygame.Rect(300, 300, 200, 40)
    pygame.draw.rect(surface, WHITE, input_box_rect, 2)
    
    input_text = font_text.render(game_state.seed_input_text, True, WHITE)
    text_x = input_box_rect.x + 5
    text_y = input_box_rect.y + (input_box_rect.height - input_text.get_height()) // 2
    surface.blit(input_text, (text_x, text_y))
    
    # Cursor
    cursor_x = text_x + input_text.get_width()
    if pygame.time.get_ticks() % 1000 < 500:
        pygame.draw.line(surface, WHITE, 
                        (cursor_x, text_y), 
                        (cursor_x, text_y + input_text.get_height()), 2)
    
    # Instructions
    instructions = [
        "ENTER - Confirm seed",
        "ESC - Cancel",
        "BACKSPACE - Delete character",
        "",
        f"Current seed: {game_state._entropy_seed}"
    ]
    
    for i, instr in enumerate(instructions):
        if instr:
            text = font_small.render(instr, True, YELLOW)
            surface.blit(text, (center_x - text.get_width() // 2, 400 + i * 25))


def display_quit_confirmation(surface, game_state):
    center_x = DISPLAY_WIDTH // 2

    # Background
    if hasattr(game_state, 'menu_bg_icon_faded') and game_state.menu_bg_icon_faded:
        icon_rect = game_state.menu_bg_icon_faded.get_rect()
        x = (DISPLAY_WIDTH - icon_rect.width) // 2
        y = (DISPLAY_HEIGHT - icon_rect.height) // 2
        surface.blit(game_state.menu_bg_icon_faded, (x, y))
    
    # Panel
    panel_width, panel_height = 500, 300
    panel_x = (DISPLAY_WIDTH - panel_width) // 2
    panel_y = (DISPLAY_HEIGHT - panel_height) // 2
    draw_panel(surface, panel_width, panel_height, panel_x, panel_y, 
               alpha=200, border_color=(128, 128, 128))
    
    # Fonts
    font_title = pygame.font.SysFont("impact", 48)
    font_text = pygame.font.SysFont("bahnschrift", 24, True)
    font_small = pygame.font.SysFont("bahnschrift", 18)
    
    # Title
    title = font_title.render("QUIT GAME?", True, RED)
    surface.blit(title, (center_x - title.get_width() // 2, 200))
    
    # Message
    message = font_text.render("Are you sure you want to quit?", True, WHITE)
    surface.blit(message, (center_x - message.get_width() // 2, 280))
    
    warning = font_small.render("Any unsaved progress will be lost.", True, YELLOW)
    surface.blit(warning, (center_x - warning.get_width() // 2, 320))
    
    # Options
    instructions = [
        "Y - Yes, quit the game",
        "N - No, go back to menu",
        "ESC - Cancel"
    ]
    
    for i, instruction in enumerate(instructions):
        color = GREEN if instruction.startswith("N") else YELLOW
        text = font_small.render(instruction, True, color)
        surface.blit(text, (center_x - text.get_width() // 2, 350 + i * 25))
