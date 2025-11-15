@echo off
title Seam Carving - Executable Builder
color 0B

echo =======================================================
echo  Seam Carving Executable Builder
echo =======================================================
echo.
echo This script will install all required Python libraries
echo (numpy, opencv-python, scipy) and then build all 5
echo .exe files using PyInstaller.
echo.
echo Make sure you have Python 3 installed and added to your
echo system's PATH.
echo.
pause
cls

REM Step 1: Install PyInstaller (the builder)
echo [Step 1/3] Installing PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller.
    echo Please make sure pip is working.
    pause
    goto end
)
echo.

REM Step 2: Install project dependencies
echo [Step 2/3] Installing project dependencies...
pip install numpy opencv-python scipy
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    goto end
)
echo.

REM Step 3: Build all executables
echo [Step 3/3] Building executables...
echo.

echo Building dynamic_programming_seam_carving.exe...
pyinstaller --onefile dynamic_programming_seam_carving.py

echo.
echo Building greedy_algorithm_seam_carving.exe...
pyinstaller --onefile greedy_algorithm_seam_carving.py

echo.
echo Building graph_cut_seam_carving.exe...
pyinstaller --onefile graph_cut_seam_carving.py

echo.
echo Building interactive_seam_carving.exe...
pyinstaller --onefile interactive_seam_carving.py

echo.
echo Building image_comparison_viewer.exe...
pyinstaller --onefile image_comparison_viewer.py

echo.
echo =======================================================
echo  BUILD COMPLETE!
echo =======================================================
echo.
echo Your .exe files are in the 'dist' folder.
echo.
echo Move the 5 .exe files from 'dist' into your
echo 'SeamCarvingApplication' folder, alongside the
echo 'SeamCarvingApp.bat' and 'images' folder.
echo.
pause

:end
exit