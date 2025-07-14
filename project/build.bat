@echo off
echo Building SpeedyHighway v1.0.1 executable with enhanced antivirus compatibility...
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
echo Starting build process with antivirus optimizations...
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
echo - Version information v1.0.1
echo - Company details and file descriptions
echo - Digital signature preparation
echo - Clean root folder placement
echo - Preserved spec file for future builds
echo - Optimized build process for antivirus compatibility
echo.
echo ANTIVIRUS COMPATIBILITY FEATURES:
echo - Proper file metadata and versioning
echo - Company information and descriptions
echo - Standard executable structure
echo - No obfuscation or packing
echo - Clear file origins and purpose
echo.
echo You can now run the game by double-clicking SpeedyHighway.exe!
echo.
pause
