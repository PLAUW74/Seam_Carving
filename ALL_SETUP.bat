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
py -m pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller.
    echo Please make sure Python is working.
    pause
    goto end
)
echo.
REM Step 2: Install project dependencies
echo [Step 2/3] Installing project dependencies...
py -m pip install numpy opencv-python scipy
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
py -m PyInstaller --onefile --hidden-import=cv2 --hidden-import=numpy.core._methods --hidden-import=numpy.lib.format dynamic_programming_seam_carving.py
echo.
echo Building greedy_algorithm_seam_carving.exe...
py -m PyInstaller --onefile --hidden-import=cv2 --hidden-import=numpy.core._methods --hidden-import=numpy.lib.format greedy_algorithm_seam_carving.py
echo.
echo Building image_comparison_viewer.exe...
py -m PyInstaller --onefile --hidden-import=cv2 --hidden-import=numpy.core._methods --hidden-import=numpy.lib.format image_comparison_viewer.py
echo.
echo =======================================================
echo  BUILD COMPLETE!
echo =======================================================
echo.
echo Your .exe files are in the 'dist' folder.
echo.
echo Move the 3 .exe files from 'dist' into your
echo 'SeamCarvingApp' folder, alongside the
echo 'run_example.bat' and 'images' folder.
echo.
pause
:end
exit