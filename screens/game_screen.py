"""
Game Screen
SpeedyHighway v1.2.0

"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from game.config import (
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    BLACK, WHITE, GREEN, RED, BLUE, YELLOW,
    DIFFICULTY_MODES
)


def display_enhanced_hud(surface, game_state):
    font = pygame.font.SysFont("consolas", 24)
    font_small = pygame.font.SysFont("consolas", 18)
    
    # Score
    score_text = font.render(f"Score: {game_state.total_score}", True, WHITE)
    surface.blit(score_text, (10, 10))
    
    # Bonus
    bonus_text = font_small.render(f"Bonus: {game_state.bonus_score}", True, YELLOW)
    surface.blit(bonus_text, (10, 35))
    
    # Near misses with flash effect
    near_miss_color = WHITE
    if game_state.near_miss_flash_timer > 0:
        near_miss_color = GREEN
        game_state.near_miss_flash_timer -= 1
    
    near_miss_text = font_small.render(f"Near Misses: {game_state.near_miss_count}", True, near_miss_color)
    surface.blit(near_miss_text, (10, 55))
    
    # Lane changes
    lane_text = font_small.render(f"Lane Changes: {game_state.lane_change_count}", True, BLUE)
    surface.blit(lane_text, (10, 75))
    
    # Speed (right side)
    speed_text = font_small.render(f"Speed: {game_state.enemy_car_speed}", True, RED)
    surface.blit(speed_text, (650, 10))
    
    # Difficulty
    diff_text = font_small.render(f"Difficulty: {DIFFICULTY_MODES[game_state.current_difficulty]}", True, WHITE)
    surface.blit(diff_text, (650, 30))
    
    # Survival time
    survival_seconds = game_state.survival_time // 60
    time_text = font_small.render(f"Time: {survival_seconds}s", True, WHITE)
    surface.blit(time_text, (650, 50))


def display_pause_menu(surface):
    # Overlay
    overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    # Pause text
    font = pygame.font.SysFont("impact", 72, True)
    pause_text = font.render("PAUSED", True, WHITE)
    surface.blit(pause_text, (400 - pause_text.get_width() // 2, 200 - pause_text.get_height() // 2))
    
    # Instructions
    font_small = pygame.font.SysFont("consolas", 20)
    instruction1 = font_small.render("Press ESC to Resume", True, WHITE)
    instruction2 = font_small.render("Click on window to resume", True, WHITE)
    surface.blit(instruction1, (400 - instruction1.get_width() // 2, 280))
    surface.blit(instruction2, (400 - instruction2.get_width() // 2, 310))


def display_countdown_timer(surface, unpause_timer):
    countdown_number = (unpause_timer // 60) + 1
    
    # Overlay
    overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    overlay.set_alpha(100)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    # Countdown number
    font = pygame.font.SysFont("impact", 120, True)
    countdown_text = font.render(str(countdown_number), True, WHITE)
    surface.blit(countdown_text, (400 - countdown_text.get_width() // 2, 300 - countdown_text.get_height() // 2))
    
    # Ready text
    font_small = pygame.font.SysFont("consolas", 36, True)
    ready_text = font_small.render("Get Ready!", True, WHITE)
    surface.blit(ready_text, (400 - ready_text.get_width() // 2, 200 - ready_text.get_height() // 2))


def display_credit(surface):
    from game.config import __version__
    
    font = pygame.font.SysFont("consolas", 14)
    text = font.render(f"SpeedyHighway v{__version__}", True, WHITE)
    surface.blit(text, (600, 500))
    text = font.render("Thanks & Regards,", True, WHITE)
    surface.blit(text, (600, 520))
    text = font.render("Tanay Vidhate", True, WHITE)
    surface.blit(text, (600, 540))
    text = font.render("(WARlord05)", True, WHITE)
    surface.blit(text, (600, 560))
