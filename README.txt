SPEEDY HIGHWAY - RACING GAME v1.0.1 Enhanced Edition
====================================================

OVERVIEW
--------
A 2D racing game built with Python and Pygame featuring enhanced mechanics, multiple difficulty levels, 
achievement system, car unlocking, and persistent game data storage with robust error handling.

✅ WHAT YOU HAVE:
- SpeedyHighway.exe - Fully portable game executable
- All assets and data files bundled inside the executable
- No Python installation required on target computers
- Works on any Windows system (64-bit)
- Enhanced antivirus compatibility features

HOW TO RUN THE GAME
-------------------
1. Navigate to the SpeedyHighway folder
2. Double-click SpeedyHighway.exe
3. Use the menu to navigate:
   - SPACE: Start Game
   - H: High Scores
   - A: Achievements
   - C: Car Selection
   - D: Difficulty Settings
   - ESC: Quit

GAME CONTROLS
-------------
- LEFT/RIGHT arrows: Move car between lanes
- ESC: Pause/Resume game
- Mouse click: Resume from pause

GAME FEATURES
-------------
✅ Multi-lane highway racing with progressive difficulty
✅ Near miss detection system with score bonuses
✅ Lane change tracking and scoring
✅ Survival time bonuses
✅ Enhanced HUD with detailed statistics
✅ Car selection system with unlockable vehicles
✅ Achievement system with various challenges
✅ Daily challenges
✅ High score tracking per difficulty
✅ Pause/resume functionality
✅ Auto-save game progress

DIFFICULTY LEVELS
-----------------
- Easy: Speed multiplier 0.7x
- Normal: Speed multiplier 1.0x (default)
- Hard: Speed multiplier 1.3x
- Insane: Speed multiplier 1.6x

DISTRIBUTION & SHARING
----------------------
✅ DIRECT SHARING: Copy SpeedyHighway.exe to any location and run
✅ USB/PORTABLE: Copy to USB drive and run from any Windows computer
✅ GAME FOLDER: Create a folder, copy the exe, and include this README

🛡️ ANTIVIRUS FALSE POSITIVE SOLUTIONS
=====================================

If your antivirus software flags SpeedyHighway.exe as suspicious, this is a FALSE POSITIVE.

WHY THIS HAPPENS:
- PyInstaller bundles Python runtime, which some antivirus software incorrectly flags
- The executable is unsigned, which triggers heuristic detection
- This is a VERY common issue with Python executables

OUR ANTIVIRUS COMPATIBILITY MEASURES:
✅ Enhanced metadata with proper company information
✅ Disabled UPX compression (reduces false positives)
✅ Standard executable structure without obfuscation
✅ Comprehensive version information and file descriptions
✅ Clear file origins and purpose documentation

SOLUTIONS:
1. WHITELIST THE FILE (RECOMMENDED)
   - Add SpeedyHighway.exe to your antivirus whitelist/exclusions
   - For Windows Defender: Virus & threat protection → Exclusions → Add file
   - For McAfee: Real-Time Scanning → Excluded Files → Add SpeedyHighway.exe
   - For Norton: Settings → Antivirus → Exclusions → Configure → Add SpeedyHighway.exe

2. VERIFY THE FILE IS SAFE
   - File name: SpeedyHighway.exe
   - Publisher: WARlord05 Games
   - Description: Speedy Highway Racing Game - Enhanced Edition
   - Version: 1.0.1.0
   - Source: Built from open source Python code with antivirus compatibility features

3. TEMPORARY DISABLE
   - Temporarily disable real-time protection
   - Run the game
   - Re-enable protection after confirming it works

4. SUBMIT AS FALSE POSITIVE
   - Report to your antivirus vendor that this is a false positive
   - Most vendors will whitelist it after verification

VERIFICATION STEPS:
1. Check file properties - should show version info and publisher
2. File size should be approximately 27-30 MB
3. Scan with multiple antivirus engines online (like VirusTotal)
4. Source code is available for review on GitHub
5. Executable is located in root folder (SpeedyHighway.exe)

TECHNICAL INFORMATION
---------------------
Version: 1.0.1 Enhanced Edition
Author: WARlord05 (Enhanced from Tanay Vidhate's original)
Date: July 2025
Engine: Python 3.13+ with Pygame 2.6.1+
Platform: Windows 64-bit

BUILD SYSTEM (For Developers):
- Single build command: build.bat (in project folder)
- Spec file preserved: SpeedyHighway.spec
- Version info: version_info.txt (antivirus compatibility metadata)
- Executable location: Root folder (SpeedyHighway.exe)
- Antivirus compatibility: Disabled UPX, enhanced metadata

ROBUST DATA HANDLING:
The game includes comprehensive data persistence that automatically handles:
- Missing or corrupted game_data.json files
- JSON parsing errors
- Permission errors with alternative save locations
- Directory creation for data folder
- Default data structure creation

PROJECT STRUCTURE:
SpeedyHighway/
├── SpeedyHighway.exe          # Main executable (ready to run)
├── car.py                     # Source code
├── README.txt                 # This file
├── assets/                    # Game assets (bundled in exe)
├── data/                      # Game save data
├── project/                   # Build system and development files
└── docs/                      # This documentation

SUPPORT & TROUBLESHOOTING
-------------------------
- Game data is automatically created and managed
- If you experience issues, try running as administrator
- For persistent antivirus issues, use the whitelist solutions above
- Source code is available for review and modification

ENJOY THE GAME!
===============
Thank you for playing Speedy Highway v1.0.1 Enhanced Edition!

Created by WARlord05 (Enhanced from Tanay Vidhate's original)
© 2025 WARlord05 Games
