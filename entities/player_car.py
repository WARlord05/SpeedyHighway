"""
Player Car Entity
SpeedyHighway v1.2.0

Handles player car: loading, rendering, animation, and movement.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from game.utils import get_resource_path
from game.config import (
    AVAILABLE_CARS, CAR_WIDTH, CAR_START_X, 
    DISPLAY_HEIGHT, SPECIAL_CAR_FRAMES, SPECIAL_CAR_ANIMATION_SPEED
)


class PlayerCar:
    """Player car entity with animation support."""
    
    def __init__(self, car_index=0):
        self.car_index = car_index
        self.x = CAR_START_X
        self.y = int(DISPLAY_HEIGHT * 0.8)
        self.width = CAR_WIDTH
        
        # Animation for special car
        self.spc_frames = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = SPECIAL_CAR_ANIMATION_SPEED
        
        # Load car image
        self.image = None
        self.load_car_image(car_index)
    
    def load_car_image(self, car_index):
        """Load car image based on car index."""
        self.car_index = car_index
        car_filename = AVAILABLE_CARS[car_index]
        
        if car_filename == "special":
            self._load_special_car()
        else:
            self._load_standard_car(car_filename)
    
    def _load_special_car(self):
        """Load animated special car frames."""
        try:
            self.spc_frames = []
            for i in range(SPECIAL_CAR_FRAMES):
                frame_path = get_resource_path(os.path.join("assets", "spc", f"spc{i}.png"))
                frame_img = pygame.image.load(frame_path)
                self.spc_frames.append(frame_img)
            self.image = self.spc_frames[0]
            self.current_frame = 0
        except pygame.error:
            print("Warning: Special car images not found. Using fallback.")
            self.image = pygame.image.load(
                get_resource_path(os.path.join("assets", "car_yellow.png"))
            )
            self.spc_frames = []
    
    def _load_standard_car(self, filename):
        """Load standard car image."""
        self.image = pygame.image.load(
            get_resource_path(os.path.join("assets", filename))
        )
        self.spc_frames = []
    
    def update_animation(self):
        """Update special car animation frame."""
        if self.spc_frames:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.spc_frames)
                self.image = self.spc_frames[self.current_frame]
    
    def draw(self, surface):
        """Draw the car on the given surface."""
        surface.blit(self.image, (self.x, self.y))
    
    def move_left(self, amount=80):
        """Move car left by amount."""
        self.x -= amount
    
    def move_right(self, amount=80):
        """Move car right by amount."""
        self.x += amount
    
    def set_position(self, x, y):
        """Set car position."""
        self.x = x
        self.y = y
    
    def get_rect(self):
        """Get car bounding rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.image.get_height())
