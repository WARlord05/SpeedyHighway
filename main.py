"""
SpeedyHighway - Main Entry Point
v1.2.0

"""

import os
import warnings

# Remove pygame support message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
warnings.filterwarnings('ignore')

from game.core import CarRacing

def main():
    game = CarRacing()
    game.racing_window()

if __name__ == "__main__":
    main()
