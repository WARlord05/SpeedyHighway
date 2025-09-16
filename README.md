# 🏎️ Speedy Highway - Racing Game v1.1.0

[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](https://github.com/WARlord05/SpeedyHighway)
[![Version](https://img.shields.io/badge/Version-1.1.0-blue)](https://github.com/WARlord05/SpeedyHighway/releases)
[![Platform](https://img.shields.io/badge/Platform-Windows%2064--bit-lightgrey)](https://github.com/WARlord05/SpeedyHighway)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/WARlord05/SpeedyHighway/blob/main/LICENSE)

## 🎮 Overview

A thrilling 2D highway racing game built with Python and Pygame featuring enhanced mechanics, multiple difficulty levels, achievement system, car unlocking, and persistent game data storage with robust error handling. **Version 1.1.0** introduces comprehensive safety features to prevent accidental data loss.

### ✅ What You Get

- **SpeedyHighway.exe** - Fully portable game executable (v1.1.0)
- Enhanced safety features with confirmation dialogs
- All assets and data files bundled inside the executable
- No Python installation required on target computers
- Works on any Windows system (64-bit)
- Enhanced antivirus compatibility features

### 🛡️ New in v1.1.0 - Enhanced Safety Features

- **Two-Step Reset Confirmation**: Prevents accidental data loss with Y/N confirmation
- **Interactive Warning Dialogs**: Clear visual feedback before destructive operations
- **Multiple Safeguards**: ESC and N key cancellation options
- **Better User Experience**: Comprehensive information about consequences before actions

## 🚀 Quick Start

### How to Run the Game

1. Navigate to the SpeedyHighway folder
2. Double-click `SpeedyHighway.exe`
3. Use the menu to navigate:
   - **SPACE**: Start Game
   - **H**: High Scores
   - **A**: Achievements
   - **C**: Car Selection
   - **D**: Difficulty Settings
   - **ESC**: Quit

### 🎯 Game Controls

- **LEFT/RIGHT arrows**: Move car between lanes
- **ESC**: Pause/Resume game or cancel confirmation dialogs
- **Mouse click**: Resume from pause

### 🛡️ Safety Features (New in v1.1.0)

- **R key** (in achievements menu): Initiate reset progress with confirmation
- **Y key** (in confirmation dialog): Confirm reset after seeing warnings
- **N key** (in confirmation dialog): Cancel reset and keep your data
- **ESC key** (in confirmation dialog): Safe cancellation option

## 🎮 Game Features

### Core Gameplay

✅ **Multi-lane highway racing** with progressive difficulty  
✅ **Near miss detection system** with score bonuses  
✅ **Lane change tracking** and scoring  
✅ **Survival time bonuses**  
✅ **Enhanced HUD** with detailed statistics  

### Advanced Features

✅ **Car selection system** with unlockable vehicles  
✅ **Achievement system** with various challenges  
✅ **Daily challenges** for extra excitement  
✅ **High score tracking** per difficulty  
✅ **Pause/resume functionality**  
✅ **Auto-save game progress**  
✅ **Enhanced Reset Progress** with confirmation dialogs (NEW in v1.1.0)  
✅ **Two-step safety confirmation** prevents accidental data loss  

## 🏁 Difficulty Levels

| Level | Speed Multiplier | Description |
|-------|------------------|-------------|
| **Easy** | 0.7x | Perfect for beginners |
| **Normal** | 1.0x | Balanced gameplay (default) |
| **Hard** | 1.3x | Increased challenge |
| **Insane** | 1.6x | Ultimate test of skill |

## 🏆 Achievement System

Complete 9 different achievements to test your skills:

| Achievement | Description |
|-------------|-------------|
| **First Drive** | Complete your first game |
| **Road Warrior** | Score 1000+ points |
| **Highway Legend** | Score 5000+ points |
| **Close Call** | Get 10 near misses in one game |
| **Lane Master** | Change lanes 50 times in one game |
| **Survivor** | Survive for 2 minutes |
| **Speed Demon** | Reach maximum speed for your difficulty |
| **Speed God** | Reach speed 40 in Insane difficulty |
| **Perfect Game** | Complete the daily challenge |

## 🚗 Car Collection

Unlock new cars by achieving high scores:

| Car | Unlock Requirement | Description |
|-----|-------------------|-------------|
| **Default Car** | Available from start | Classic racing car |
| **Blue Racer** | Score 500+ points | Sleek blue design |
| **Red Speed** | Score 1500+ points | High-performance red car |
| **Yellow Lightning** | Score 3000+ points | Ultimate speed machine |

## 🆕 What's New in Version 1.1.0

### 🛡️ Enhanced Safety Features

- **Two-Step Reset Confirmation**: Added comprehensive Y/N confirmation dialog before resetting progress
- **Clear Visual Warnings**: Red warning text with detailed information about data deletion consequences
- **Multiple Safeguards**: ESC and N key both provide safe cancellation options
- **Interactive Experience**: Full-screen confirmation dialog with clear choices before any destructive operations

### 🎯 Improved User Experience

- **Accident Prevention**: No more accidental progress resets
- **Better Feedback**: Clear visual indicators for all user actions
- **Enhanced Safety**: Multiple opportunities to cancel before data loss
- **Maintained Performance**: All new features with zero impact on game performance

### 🔧 Technical Improvements

- Updated to version 1.1.0 with enhanced build metadata
- Improved confirmation dialog system architecture
- Enhanced state management for safety features
- Backward compatible with all existing save files

## 📦 Distribution & Sharing

### Easy Sharing Options

✅ **Direct Sharing**: Copy `SpeedyHighway.exe` to any location and run  
✅ **USB/Portable**: Copy to USB drive and run from any Windows computer  
✅ **Game Folder**: Create a folder, copy the exe, and include documentation  

## 🛡️ Antivirus False Positive Solutions

> **Important:** If your antivirus software flags `SpeedyHighway.exe` as suspicious, this is a **FALSE POSITIVE**.

### Why This Happens

- PyInstaller bundles Python runtime, which some antivirus software incorrectly flags
- The executable is unsigned, which triggers heuristic detection
- This is a **very common issue** with Python executables

### Our Antivirus Compatibility Measures

✅ Enhanced metadata with proper company information  
✅ Disabled UPX compression (reduces false positives)  
✅ Standard executable structure without obfuscation  
✅ Comprehensive version information and file descriptions  
✅ Clear file origins and purpose documentation  

### Solutions

#### 1. 🔒 Whitelist the File (Recommended)

Add `SpeedyHighway.exe` to your antivirus whitelist/exclusions:

- **Windows Defender**: Virus & threat protection → Exclusions → Add file
- **McAfee**: Real-Time Scanning → Excluded Files → Add `SpeedyHighway.exe`
- **Norton**: Settings → Antivirus → Exclusions → Configure → Add `SpeedyHighway.exe`

#### 2. ✅ Verify the File is Safe

- **File name**: `SpeedyHighway.exe`
- **Publisher**: WARlord05 Games
- **Description**: Speedy Highway Racing Game - Enhanced Edition
- **Version**: 1.1.0
- **Source**: Built from open source Python code with antivirus compatibility features

#### 3. 🔄 Verification Steps

1. Check file properties - should show version info and publisher
2. File size should be approximately 27-30 MB
3. Scan with multiple antivirus engines online (like VirusTotal)
4. Source code is available for review on GitHub
5. Executable is located in root folder (`SpeedyHighway.exe`)

## 🔧 Technical Information

### System Requirements

- **Operating System**: Windows 7/8/10/11 (64-bit recommended)
- **Memory**: 100MB RAM minimum
- **Storage**: 50MB free disk space
- **Graphics**: DirectX-compatible graphics card

### Technical Details

- **Version**: 1.1.0 Enhanced Safety Edition
- **Author**: Tanay Vidhate (WARlord05)
- **Release Date**: September 2025
- **Engine**: Python 3.13+ with Pygame 2.6.1+
- **Platform**: Windows 64-bit

### For Developers

- **Build Command**: `build.bat` (in project folder)
- **Spec File**: `SpeedyHighway.spec` (preserved)
- **Version Info**: `version_info.txt` (antivirus compatibility metadata)
- **Executable Location**: Root folder (`SpeedyHighway.exe`)
- **Antivirus Compatibility**: Disabled UPX, enhanced metadata

## 📁 Project Structure

```text
SpeedyHighway/
├── SpeedyHighway.exe          # Main executable v1.1.0 (ready to run)
├── SpeedyHighway_v1.0.1_backup.exe  # Previous version backup
├── car.py                     # Source code (v1.1.0)
├── README.md                  # This file (updated for v1.1.0)
├── RELEASE_NOTES_v1.1.0.md    # New release documentation
├── assets/                    # Game assets (bundled in exe)
├── data/                      # Game save data
├── project/                   # Build system and development files
│   ├── build.bat             # Build script
│   ├── PROJECT_STRUCTURE.txt # Technical structure details
│   └── SpeedyHighway.spec    # PyInstaller specification
└── docs/                      # Documentation
    └── PROJECT_DOCUMENTATION.md # Comprehensive documentation (updated)
```

## 🔧 Robust Data Handling

The game includes comprehensive data persistence that automatically handles:

- Missing or corrupted `game_data.json` files
- JSON parsing errors
- Permission errors with alternative save locations
- Directory creation for data folder
- Default data structure creation

## 🆘 Support & Troubleshooting

### Common Issues

- **Game Won't Start**: Try running as administrator
- **Achievements Not Unlocking**: Check achievements menu (A key)
- **Save Data Lost**: Backup `data/game_data.json` file
- **Antivirus Issues**: Use whitelist solutions above
- **Reset Confirmation**: Press Y to confirm, N or ESC to cancel (NEW in v1.1.0)

### Getting Help

- Check the [Issues](https://github.com/WARlord05/SpeedyHighway/issues) section
- Submit bug reports with system information
- Review the comprehensive documentation in `docs/`

## 📚 Documentation

- **Quick Start**: This README file
- **Release Notes**: `RELEASE_NOTES_v1.1.0.md` (NEW)
- **Technical Details**: `project/PROJECT_STRUCTURE.txt`
- **Comprehensive Guide**: `docs/PROJECT_DOCUMENTATION.md`

## 🎉 Enjoy the Game

Thank you for playing **Speedy Highway v1.1.0 Enhanced Safety Edition**!

**🆕 New in v1.1.0**: Enhanced safety features prevent accidental data loss while maintaining all the excitement of high-speed racing!

---

**Created by**: Tanay Vidhate (WARlord05)  
**© 2025 WARlord05 Games**  
**Repository**: [github.com/WARlord05/SpeedyHighway](https://github.com/WARlord05/SpeedyHighway)

[![GitHub stars](https://img.shields.io/github/stars/WARlord05/SpeedyHighway?style=social)](https://github.com/WARlord05/SpeedyHighway/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/WARlord05/SpeedyHighway?style=social)](https://github.com/WARlord05/SpeedyHighway/network/members)
