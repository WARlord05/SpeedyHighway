@echo off
REM Build script for SpeedyHighway
echo Building SpeedyHighway executable...
echo.

REM Navigate to parent directory (where car.py is located)
cd /d "%~dp0\.."

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller is not installed. Installing now...
    pip install PyInstaller
) else (
    echo PyInstaller is installed
)

echo Starting build process...
pyinstaller --onefile --windowed --add-data "assets;assets" --add-data "data;data" car.py --name SpeedyHighway

REM Clean up temporary files
if exist "build" rmdir /s /q "build"
if exist "SpeedyHighway.spec" del "SpeedyHighway.spec"

echo.
echo ================================
echo BUILD SUCCESSFUL!
echo ================================
echo Your executable is located at:
echo %CD%\dist\SpeedyHighway.exe
echo You can now run the game by double-clicking SpeedyHighway.exe!
pause
