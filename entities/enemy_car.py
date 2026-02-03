"""
Enemy Car Entity
SpeedyHighway v1.2.0
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from game.utils import get_resource_path
from game.config import (
    LANE_POSITIONS, ENEMY_CAR_WIDTH, ENEMY_CAR_HEIGHT,
    ENEMY_START_Y, BASE_ENEMY_SPEED, DIFFICULTY_MULTIPLIERS
)


class EnemyCar:
    
    def __init__(self, difficulty=1, random_func=None):
        self.width = ENEMY_CAR_WIDTH
        self.height = ENEMY_CAR_HEIGHT
        
        # Use provided random function or default
        self._random_choice = random_func if random_func else self._default_choice
        
        # Position
        self.x = self._random_choice(LANE_POSITIONS)
        self.y = ENEMY_START_Y
        
        # Speed based on difficulty
        difficulty_multiplier = DIFFICULTY_MULTIPLIERS[difficulty]
        self.speed = int(BASE_ENEMY_SPEED * difficulty_multiplier)
        
        # Load image
        self.image = pygame.image.load(
            get_resource_path(os.path.join("assets", "car_black.png"))
        )
    
    def _default_choice(self, choices):
        import random
        return random.choice(choices)
    
    def update(self):
        self.y += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    
    def is_off_screen(self, screen_height):
        return self.y > screen_height
    
    def reset(self, random_func=None):
        if random_func:
            self._random_choice = random_func
        self.x = self._random_choice(LANE_POSITIONS)
        self.y = ENEMY_START_Y
    
    def set_speed(self, speed):
        self.speed = speed
    
    def increase_speed(self, amount=1):
        self.speed += amount
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def check_collision(self, player_x, player_y, player_width):
        if (self.y + self.height > player_y and 
            self.y < player_y + 100):  
            if (self.x + self.width > player_x and 
                self.x < player_x + player_width):
                return True
        return False
    
    def check_near_miss(self, player_x, player_y, threshold_x=50, threshold_y=100):
        return (abs(player_x - self.x) <= threshold_x and 
                abs(player_y - self.y) <= threshold_y)
