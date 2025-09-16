SpeedyHighway v1.1.0 - Technical Project Structure
=================================================

Author: Tanay Vidhate (WARlord05)
Date: September 16, 2025
Status: Production Ready - Enhanced Safety Edition

DIRECTORY STRUCTURE
===================

SpeedyHighway/
├── car.py                      # Main game source code (v1.1.0)
├── SpeedyHighway.exe           # Built executable v1.1.0 (production ready)
├── SpeedyHighway_v1.0.1_backup.exe # Previous version backup
├── README.md                   # Project overview and quick start guide
├── RELEASE_NOTES_v1.1.0.md     # Version 1.1.0 release documentation
├── assets/                     # Game assets directory
│   ├── back.jpg               # Background road image
│   ├── car.png                # Default player car sprite
│   ├── car_blue.png           # Blue car sprite (unlockable)
│   ├── car_red.png            # Red car sprite (unlockable)
│   ├── car_yellow.png         # Yellow car sprite (unlockable)
│   └── spc/                   # Special car animation frames
│       ├── spc0.png           # Special car frame 0
│       ├── spc1.png           # Special car frame 1
│       └── ...                # Frames 2-11 for 12-frame animation
├── data/                      # Game data and save files
│   └── game_data.json         # Player progress, achievements, scores
├── docs/                      # Documentation directory
│   ├── PROJECT_DOCUMENTATION.md # Comprehensive project documentation
│   └── PROJECT_STRUCTURE.md  # This file (technical structure details)
└── project/                   # Build system and development files
    ├── build.bat              # Main build script
    ├── SpeedyHighway.spec     # PyInstaller specification
    ├── version_info.py        # Version information module (v1.1.0)
    └── version_info.txt       # Executable metadata for antivirus compatibility (v1.1.0)

CORE COMPONENTS
===============

Main Game File (car.py)
-----------------------

- Total Lines: Updated for v1.1.0
- Language: Python 3.13+
- Dependencies: pygame, json, os, sys, random, datetime

Key Classes:

- GameStates: Enum for game state management
- Achievement: Achievement data structure
- CarRacing: Main game class with complete functionality

Key Features:

- Multi-state game management (Menu, Playing, Paused, GameOver, etc.)
- 9 different achievements with persistent saving
- 4 difficulty levels with progressive speed increases
- Car selection system with 4 unlockable vehicles
- Enhanced scoring system with bonuses
- Daily challenge system
- High score tracking per difficulty
- Enhanced reset progress functionality with confirmation dialogs (NEW v1.1.0)
- Two-step safety confirmation system (NEW v1.1.0)
- Robust data persistence with error handling

GAME DATA STRUCTURE
==================

game_data.json contains:

- high_scores: Array of top 10 scores with metadata
- difficulty: Current difficulty level (0-3)
- selected_car: Currently selected car index
- unlocked_cars: Array of unlocked car indices
- achievements: Object mapping achievement IDs to unlock status
- games_played: Total number of games played
- total_playtime: Cumulative survival time across all games
- best_streak: Best consecutive games streak
- last_daily_challenge: Date of last daily challenge generation
- daily_challenge: Current daily challenge data
- highest_difficulty_reached: Highest difficulty ever played
- best_scores_per_difficulty: Array of best scores for each difficulty

ACHIEVEMENT SYSTEM
==================

Achievement IDs and Descriptions:

- first_game: "First Drive" - Play your first game
- score_1000: "Road Warrior" - Score 1000 points
- score_5000: "Highway Legend" - Score 5000 points
- near_miss_10: "Close Call" - Get 10 near misses in one game
- lane_master: "Lane Master" - Change lanes 50 times in one game
- survivor: "Survivor" - Survive for 2 minutes (7200 frames)
- speed_demon: "Speed Demon" - Reach maximum speed for difficulty
- speed_god: "Speed God" - Reach 40 speed in Insane difficulty
- perfect_game: "Perfect Game" - Complete daily challenge

Achievement Features:

- Persistent saving to JSON file
- Automatic checking during gameplay
- Visual feedback with color coding
- Reset functionality with progress warning

DIFFICULTY SYSTEM
================

Difficulty Levels:
0. Easy (0.7x speed multiplier)

1. Normal (1.0x speed multiplier) - Default
2. Hard (1.3x speed multiplier)
3. Insane (1.6x speed multiplier)

Speed Progression:

- Easy: Enemy speed 5→10, Background speed 3→7
- Normal: Enemy speed 5→15, Background speed 3→12
- Hard: Enemy speed 6→18, Background speed 4→15
- Insane: Enemy speed 8→unlimited, Background speed 5→unlimited

CAR UNLOCK SYSTEM
================

Car Unlock Requirements:

- Car 0 (Default): Always available
- Car 1 (Blue): Score 500+ points
- Car 2 (Red): Score 1500+ points
- Car 3 (Yellow): Score 3000+ points

Car Selection Features:

- Preview system with visual car display
- Navigation with arrow keys
- Persistent selection saving
- Unlocked car tracking

CONTROLS AND INPUT
=================

Menu Navigation:

- SPACE: Start Game
- H: High Scores
- A: Achievements
- C: Car Selection
- D: Cycle Difficulty
- ESC: Quit

Gameplay Controls:

- LEFT/RIGHT: Move car between lanes
- ESC: Pause/Resume
- Mouse Click: Resume from pause

Achievement Menu:

- ESC: Return to menu
- R: Initiate reset progress (NEW v1.1.0 - opens confirmation dialog)

Reset Progress Confirmation (NEW v1.1.0):

- Y: Confirm reset and delete all data
- N: Cancel reset and keep data
- ESC: Cancel reset and return to achievements menu

Car Selection:

- LEFT/RIGHT: Navigate cars
- SPACE: Select car
- ESC: Return to menu

SCORING SYSTEM
==============

Base Score: Survival time (count variable)
Bonus Points:

- Near Miss: 10 points each
- Lane Change: 2 points each
- Survival Bonus: 50 points per minute

Final Score Calculation:
total_score = (base_score + bonus_score) * difficulty_multiplier

Difficulty Multipliers:

- Easy: 1.0x
- Normal: 1.2x
- Hard: 1.5x
- Insane: 2.0x

DAILY CHALLENGE SYSTEM
=====================

Challenge Types:

- Score Challenge: Reach specific score target
- Survival Challenge: Survive for specific time
- Near Miss Challenge: Get specific number of near misses
- Lane Change Challenge: Change lanes specific number of times

Challenge Features:

- Daily generation with date tracking
- Persistent saving across sessions
- Completion tracking for achievements
- Random challenge selection

BUILD SYSTEM
============

Build Process:

1. Run build.bat from project folder
2. PyInstaller creates executable with metadata
3. Automatic cleanup of build artifacts
4. Spec file preserved for consistency

Antivirus Compatibility:

- Comprehensive version information
- Disabled UPX compression
- Standard executable structure
- Clear file origins and descriptions

RECENT IMPROVEMENTS
==================

Version 1.1.0 - Enhanced Safety Edition (September 16, 2025):

- Enhanced reset progress functionality with confirmation dialogs
- Two-step safety confirmation system (Y/N prompts)
- ESC cancellation support in all confirmation dialogs
- Improved user experience with clear visual warnings
- Prevention of accidental data loss through enhanced UI flow
- Maintained all existing functionality with added safety layers

Version 1.0.1 and Earlier Improvements:

Data Synchronization Fixes:

- Fixed achievement persistence after reset
- Enhanced game data synchronization
- Improved error handling for data operations
- Fixed daily challenge persistence

Achievement System Enhancements:

- Added automatic save on achievement unlock
- Fixed "First Drive" achievement after reset
- Enhanced achievement checking with change tracking
- Improved achievement notification system

Reset Progress Feature:

- Complete game data reset functionality
- Proper data synchronization after reset
- Visual warning for destructive operation
- Comprehensive state restoration

Error Handling Improvements:

- Robust JSON file handling
- Fallback data creation on corruption
- Graceful handling of missing files
- Comprehensive error logging

MAINTENANCE NOTES
================

File Preservation:

- Keep SpeedyHighway.spec for consistent builds
- Preserve version_info.txt for metadata
- Maintain data/ folder for player progress
- Assets folder contains all game sprites

Development Guidelines:

- Achievement system supports easy expansion
- Car system supports additional vehicles
- Daily challenge system can be enhanced
- Scoring system is modular and extensible

Performance Considerations:

- 60 FPS target with vsync
- Efficient sprite handling
- Optimized collision detection
- Minimal memory allocation during gameplay

TECHNICAL SPECIFICATIONS
========================

Current Version: 1.1.0 Enhanced Safety Edition

Minimum Requirements:

- Python 3.13+ (development)
- Pygame 2.6.1+
- 50MB free disk space
- 100MB RAM
- DirectX-compatible graphics

Build System:

- PyInstaller 6.14.2
- Enhanced antivirus compatibility
- Comprehensive version metadata
- Automated build process via build.bat

File Sizes:

- car.py: ~35KB (main source, v1.1.0)
- SpeedyHighway.exe: ~15-20MB (built executable, v1.1.0)
- Assets: ~500KB total
- Documentation: ~50KB total

Performance Metrics:

- Startup time: <2 seconds
- Memory usage: <100MB
- CPU usage: <10% on modern systems
- Frame rate: Consistent 60 FPS

New in v1.1.0:

- Enhanced safety confirmation system
- Two-step reset process with Y/N prompts
- ESC cancellation support
- Improved user experience and data protection

END OF DOCUMENTATION
===================
