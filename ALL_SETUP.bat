@echo off
title Seam Carving - Executable Builder & Setup (VENV)
color 0B

echo =======================================================
echo  Seam Carving Executable Builder & Setup (VENV)
echo =======================================================
echo.
echo Your Python installation is not finding modules correctly.
echo This script will now create a temporary Virtual Environment (venv)
echo to build the executables in a clean, isolated space.
echo.
pause
cls

REM Step 1: Create a temporary virtual environment
echo [Step 1/7] Creating temporary virtual environment (venv)...
py -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment.
    pause
    goto end
)
echo.

REM Step 2: Activate the virtual environment
echo [Step 2/7] Activating virtual environment...
call "venv\Scripts\activate.bat"
echo.

REM Step 3: Install PyInstaller (inside venv)
echo [Step 3/7] Installing PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller.
    pause
    goto end
)
echo.

REM Step 4: Install project dependencies (inside venv)
echo [Step 4/7] Installing project dependencies...
pip install numpy opencv-python scipy
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    goto end
)
echo.

REM Step 5: Build all executables (using venv's pyinstaller)
echo [Step 5/7] Building executables...
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

REM Step 6: Move executables
echo [Step 6/7] Moving executables to 'SeamCarvingApp' folder...
move /Y "dist\dynamic_programming_seam_carving.exe" "SeamCarvingApp\"
move /Y "dist\greedy_algorithm_seam_carving.exe" "SeamCarvingApp\"
move /Y "dist\graph_cut_seam_carving.exe" "SeamCarvingApp\"
move /Y "dist\interactive_seam_carving.exe" "SeamCarvingApp\"
move /Y "dist\image_comparison_viewer.exe" "SeamCarvingApp\"
echo.

REM Step 7: Clean up
echo [Step 7/7] Cleaning up temporary build files and venv...
rmdir /S /Q dist
rmdir /S /Q build
rmdir /S /Q venv
del *.spec
echo.

echo =======================================================
echo  BUILD AND SETUP COMPLETE!
echo =======================================================
echo.
echo All .exe files have been built and moved into the 
echo 'SeamCarvingApp' folder.
echo.
pause

:end
exit