@echo off
title "Seam Carving - Executable Builder & Setup (Portable)"
color 0B

set LOGFILE=build_log.txt
echo This script will build all 6 executables and log output to %LOGFILE%.
echo Deleting old log file...
del %LOGFILE% 2>nul
echo.

REM --- Step 0: Clean up old build files ---
echo [Step 0/6] Cleaning up old build files...
rmdir /S /Q dist
rmdir /S /Q build
del *.spec
echo.

pause
cls

REM Step 1: Install PyInstaller
echo [Step 1/6] Installing PyInstaller...
.\python_portable\python.exe -m pip install pyinstaller >> %LOGFILE% 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller. Check %LOGFILE%.
    pause
    goto end
)
echo.

REM Step 2: Install project dependencies
echo [Step 2/6] Installing project dependencies...
.\python_portable\python.exe -m pip install numpy opencv-python scipy >> %LOGFILE% 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies. Check %LOGFILE%.
    pause
    goto end
)
echo.

REM Step 3: Build all executables
echo [Step 3/6] Building executables... (This may take a while)
echo.

echo   Building SeamCarvingApp.exe (The New Launcher)...
.\python_portable\python.exe -m PyInstaller --onefile SeamCarvingApp.py >> %LOGFILE% 2>&1

echo   Building dynamic_programming_seam_carving.exe...
.\python_portable\python.exe -m PyInstaller --onefile --collect-data cv2 dynamic_programming_seam_carving.py >> %LOGFILE% 2>&1

echo   Building greedy_algorithm_seam_carving.exe...
.\python_portable\python.exe -m PyInstaller --onefile --collect-data cv2 greedy_algorithm_seam_carving.py >> %LOGFILE% 2>&1

echo   Building graph_cut_seam_carving.exe... (Fixing SciPy Shortest Path)
REM --- THIS IS THE UPDATED LINE ---
.\python_portable\python.exe -m PyInstaller --onefile --collect-data cv2 --hidden-import="scipy.sparse.csgraph._shortest_path" graph_cut_seam_carving.py >> %LOGFILE% 2>&1

echo   Building interactive_seam_carving.exe... (Fixing local import)
.\python_portable\python.exe -m PyInstaller --onefile --collect-data cv2 --paths=. interactive_seam_carving.py >> %LOGFILE% 2>&1

echo   Building image_comparison_viewer.exe...
.\python_portable\python.exe -m PyInstaller --onefile --collect-data cv2 image_comparison_viewer.py >> %LOGFILE% 2>&1
echo.

REM Step 4: Move executables (with error checking)
echo [Step 4/6] Moving executables to 'SeamCarvingApp' folder...

if not exist "dist\SeamCarvingApp.exe" ( echo ERROR: SeamCarvingApp.exe FAILED TO BUILD. Check %LOGFILE%. & pause & goto end )
move /Y "dist\SeamCarvingApp.exe" "SeamCarvingApp\"

if not exist "dist\dynamic_programming_seam_carving.exe" ( echo ERROR: dynamic_programming_seam_carving.exe FAILED TO BUILD. Check %LOGFILE%. & pause & goto end )
move /Y "dist\dynamic_programming_seam_carving.exe" "SeamCarvingApp\"

if not exist "dist\greedy_algorithm_seam_carving.exe" ( echo ERROR: greedy_algorithm_seam_carving.exe FAILED TO BUILD. Check %LOGFILE%. & pause & goto end )
move /Y "dist\greedy_algorithm_seam_carving.exe" "SeamCarvingApp\"

if not exist "dist\graph_cut_seam_carving.exe" ( echo ERROR: graph_cut_seam_carving.exe FAILED TO BUILD. Check %LOGFILE%. & pause & goto end )
move /Y "dist\graph_cut_seam_carving.exe" "SeamCarvingApp\"

if not exist "dist\interactive_seam_carving.exe" ( echo ERROR: interactive_seam_carving.exe FAILED TO BUILD. Check %LOGFILE%. & pause & goto end )
move /Y "dist\interactive_seam_carving.exe" "SeamCarvingApp\"

if not exist "dist\image_comparison_viewer.exe" ( echo ERROR: image_comparison_viewer.exe FAILED TO BUILD. Check %LOGFILE%. & pause & goto end )
move /Y "dist\image_comparison_viewer.exe" "SeamCarvingApp\"
echo.

REM Step 5: Clean up
echo [Step 5/6] Cleaning up temporary build files...
rmdir /S /Q dist
rmdir /S /Q build
del *.spec
echo.

echo =======================================================
echo " BUILD AND SETUP COMPLETE!"
echo =======================================================
echo.
echo All .exe files have been built and moved into the 
echo 'SeamCarvingApp' folder.
echo.
echo A full log was saved to: %LOGFILE%
echo.
pause

:end
exit