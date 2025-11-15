@echo off
title Seam Carving - Executable Builder & Setup
color 0B

echo =======================================================
echo  Seam Carving Executable Builder & Setup
echo =======================================================
echo.
echo This script will:
echo 1. Install all required Python libraries.
echo 2. Build all 5 .exe files using PyInstaller.
echo 3. Automatically move the .exe files into 'SeamCarvingApp'.
echo 4. Clean up all temporary build folders and files.
echo.
echo Make sure you have Python 3 installed and added to your
echo system's PATH.
echo.
pause
cls

REM Step 1: Install PyInstaller (the builder)
echo [Step 1/5] Installing PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller.
    echo Please make sure pip is working.
    pause
    goto end
)
echo.

REM Step 2: Install project dependencies
echo [Step 2/5] Installing project dependencies...
pip install numpy opencv-python scipy
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    goto end
)
echo.

REM Step 3: Build all executables
echo [Step 3/5] Building executables...
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

REM Step 4: Move executables to the application folder
echo [Step 4/5] Moving executables to 'SeamCarvingApp' folder...
REM The /Y flag overwrites existing files without prompting
move /Y "dist\dynamic_programming_seam_carving.exe" "SeamCarvingApp\"
move /Y "dist\greedy_algorithm_seam_carving.exe" "SeamCarvingApp\"
move /Y "dist\graph_cut_seam_carving.exe" "SeamCarvingApp\"
move /Y "dist\interactive_seam_carving.exe" "SeamCarvingApp\"
move /Y "dist\image_comparison_viewer.exe" "SeamCarvingApp\"
echo.

REM Step 5: Clean up temporary build files and folders
echo [Step 5/5] Cleaning up temporary build files...
REM /S deletes all subfolders. /Q runs in quiet mode.
rmdir /S /Q dist
rmdir /S /Q build
del *.spec
echo.

REM -------------------------------------------------------
REM --- END NEW SECTION ---
REM -------------------------------------------------------

echo =======================================================
echo  BUILD AND SETUP COMPLETE!
echo =======================================================
echo.
echo All .exe files have been built and moved into the
echo 'SeamCarvingApp' folder.
echo.
echo The temporary 'dist', 'build', and '.spec' files
echo have been deleted.
echo.
pause

:end
exit