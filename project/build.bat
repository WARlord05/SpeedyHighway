@echo off
echo Building SpeedyHighway v1.0.1 executable with enhanced antivirus compatibility...
echo Project: Speedy Highway - Enhanced Edition
echo Author: Tanay Vidhate (WARlord05)
echo Status: Production Ready with Recent Bug Fixes and Improvements
echo.

:: Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul || (
    echo PyInstaller not found! Installing...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo PyInstaller is installed
echo Starting build process with optimizations...
echo.

:: Clean previous build and root executable
if exist "..\build" rmdir /s /q "..\build"
if exist "..\dist" rmdir /s /q "..\dist"
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "..\SpeedyHighway.exe" del /f /q "..\SpeedyHighway.exe"

:: Build with spec file for better metadata and antivirus compatibility
python -m PyInstaller --clean --log-level=INFO SpeedyHighway.spec

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Moving executable to root folder...
:: Move executable to root folder
if exist "dist\SpeedyHighway.exe" (
    move "dist\SpeedyHighway.exe" "..\SpeedyHighway.exe"
    echo Executable moved to root folder successfully!
) else (
    echo ERROR: Executable not found in dist folder!
    pause
    exit /b 1
)

echo.
echo Cleaning up build files (preserving spec file)...
:: Clean up build directories and files (but keep spec file)
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "..\build" rmdir /s /q "..\build"
if exist "..\dist" rmdir /s /q "..\dist"

echo Build cleanup completed!
echo.
echo ================================
echo BUILD SUCCESSFUL!
echo ================================
echo Your executable is located at:
echo %cd%\..\SpeedyHighway.exe
echo.
echo This version includes:
echo - Enhanced metadata to reduce antivirus false positives
echo - Version information v1.0.1 with Enhanced Edition branding
echo - Company details and comprehensive file descriptions
echo - Digital signature preparation and clean structure
echo - Clean root folder placement for easy access
echo - Preserved spec file for consistent future builds
echo - Optimized build process for maximum antivirus compatibility
echo - Recent bug fixes and achievement system improvements
echo - Enhanced data persistence and synchronization
echo - Reset progress functionality with proper data handling
echo.
echo ANTIVIRUS COMPATIBILITY FEATURES:
echo - Proper file metadata and comprehensive versioning
echo - Company information and detailed descriptions
echo - Standard executable structure without obfuscation
echo - No compression or packing (UPX disabled)
echo - Clear file origins, purpose, and authorship
echo - Enhanced build process for security software compatibility
echo.
echo RECENT IMPROVEMENTS INCLUDED:
echo - Fixed achievement system persistence after data reset
echo - Enhanced data synchronization between JSON and memory
echo - Improved "First Drive" achievement functionality
echo - Added comprehensive reset progress feature
echo - Enhanced daily challenge system persistence
echo - Robust error handling and graceful recovery
echo - Optimized performance with reduced file I/O
echo - Better user experience with visual feedback
echo.
echo You can now run the game by double-clicking SpeedyHighway.exe!
echo.
echo GAME FEATURES:
echo - 9 different achievements with persistent saving
echo - 4 difficulty levels with progressive gameplay
echo - 4 unlockable cars with score-based progression
echo - Enhanced scoring system with bonuses and multipliers
echo - Daily challenge system with completion tracking
echo - Reset progress functionality (R key in achievements menu)
echo - Comprehensive high score tracking per difficulty
echo - Robust data persistence with error recovery
echo.
echo For comprehensive documentation see: docs/PROJECT_DOCUMENTATION.md
echo For technical structure details see: project/PROJECT_STRUCTURE.txt
echo.
pause
