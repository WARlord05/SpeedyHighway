# SpeedyHighway v1.0.1 - Project Documentation

## Project Overview
SpeedyHighway is a racing game built with Python and Pygame, featuring enhanced gameplay mechanics, multiple difficulty levels, and a comprehensive build system optimized for antivirus compatibility.

**Status**: ✅ Production Ready v1.0.1  
**Author**: WARlord05 (Enhanced from Tanay Vidhate's original)  
**Date**: July 2025  

## Build System

### Current Build Configuration
- **Single Build File**: `build.bat` (sole build script)
- **Spec File**: `SpeedyHighway.spec` (preserved for consistency)
- **Version Info**: `version_info.txt` (antivirus compatibility metadata)

### Build Process
1. Run `build.bat` from the project folder
2. Executable created at: `SpeedyHighway.exe` (in root folder)
3. Automatic cleanup of build files while preserving spec file

### Antivirus Compatibility Features
- Enhanced metadata with company information
- Disabled UPX compression (reduces false positives)
- Standard executable structure without obfuscation
- Comprehensive version information and file descriptions
- Clear file origins and purpose documentation

## Project Structure
```
SpeedyHighway/
├── car.py                 # Main game source code
├── SpeedyHighway.exe      # Built executable
├── assets/               # Game assets (images, sounds)
├── data/                 # Game data and save files
├── docs/                 # Documentation
└── project/              # Build system and development files
    ├── build.bat         # Main build script
    ├── SpeedyHighway.spec # PyInstaller specification
    ├── version_info.txt   # Executable metadata
    └── version_info.py    # Version information module
```

## Game Features

### Core Gameplay
- Multi-lane highway racing with progressive difficulty
- Near miss detection system with score bonuses
- Lane change tracking and scoring
- Survival time bonuses
- Enhanced HUD with detailed statistics

### Difficulty Levels
- **Easy**: Speed multiplier 0.7x
- **Normal**: Speed multiplier 1.0x (default)
- **Hard**: Speed multiplier 1.3x
- **Insane**: Speed multiplier 1.6x

### Scoring System
- Base score from survival time
- Near miss bonuses (10 points each)
- Lane change bonuses (2 points each)
- Survival time bonuses (50 points per minute)
- Difficulty multipliers applied to final score

### Additional Features
- Car selection system with unlockable vehicles
- Achievement system with various challenges
- Daily challenges
- High score tracking per difficulty
- Pause/resume functionality
- Auto-save game progress

## Technical Implementation

### Key Components
- **GameStates**: Menu, Playing, Paused, GameOver, HighScores, Achievements, CarSelection
- **Enhanced Input**: Smooth movement with key repeat handling
- **Data Persistence**: JSON-based save system with error handling
- **Resource Management**: PyInstaller-compatible asset loading
- **Performance**: 60 FPS game loop with optimized rendering

### Dependencies
- Python 3.13+
- Pygame 2.6.1+
- PyInstaller 6.14.2+ (for building)

## Development History

### Version 1.0.1 - Enhanced Edition (July 15, 2025)

#### Core Game Updates:
- Added version information (`__version__ = "1.0.1"`)
- Updated window title to include version
- Enhanced menu with version display
- Fixed UI positioning (title/version overlap resolved)
- Updated credit display with version info

#### Build System Improvements:
- Enhanced build system with antivirus compatibility
- Streamlined to single build file (`build.bat`)
- Improved executable metadata
- Preserved spec file for consistent builds
- Disabled UPX compression (reduces false positives)
- Standard executable structure without obfuscation
- Comprehensive version information and file descriptions

#### Project Organization:
- Comprehensive project documentation
- Removed redundant build scripts
- Enhanced antivirus compatibility features
- Automatic cleanup with file preservation
- Single-command build process
- Detailed build logging and feedback

### Build System Evolution
- Consolidated from multiple build files to single `build.bat`
- Enhanced antivirus compatibility features
- Automatic cleanup with file preservation
- Single-command build process
- Detailed build logging and feedback

## Usage Instructions

### Running the Game
1. Double-click `SpeedyHighway.exe` to start
2. Use menu options to navigate:
   - SPACE: Start Game
   - H: High Scores
   - A: Achievements
   - C: Car Selection
   - D: Difficulty Settings
   - ESC: Quit

### Building from Source
1. Navigate to project folder
2. Run `build.bat`
3. Executable will be created in root folder

### Controls
- LEFT/RIGHT arrows: Move car between lanes
- ESC: Pause/Resume game
- Mouse click: Resume from pause

## Maintenance Notes

### File Management
- Keep `SpeedyHighway.spec` for consistent builds
- `version_info.txt` contains executable metadata
- Build artifacts are auto-cleaned except spec file
- Data files are preserved in `data/` folder

### Future Development
- Spec file preserved for easy rebuilds
- Modular code structure supports extensions
- Achievement system can be expanded
- Car selection system supports additional vehicles
- Daily challenge system can be enhanced

---
*This documentation consolidates all project information into a single reference file.*
