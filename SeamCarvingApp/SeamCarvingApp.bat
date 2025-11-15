@echo off
title Seam Carving Tool
color 0A

:menu
cls
echo ========================================
echo         SEAM CARVING TOOL
echo ========================================
echo.
echo Place your images in the 'images' folder.
echo.
echo Choose an option:
echo.
echo [Standard Algorithms]
echo 1. Dynamic Programming (Optimal, Recommended)
echo 2. Greedy Algorithm (Fast, Low-Quality)
echo 3. Graph-Cut (Bonus, Slower than DP)
echo.
echo [Bonus Tools]
echo 4. Interactive Resizing Tool (DP)
echo    (NOTE: Can be slow, re-calculates on every change)
echo 5. Exit
echo.
set "choice="
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" set exe=dynamic_programming_seam_carving.exe& goto input_params
if "%choice%"=="2" set exe=greedy_algorithm_seam_carving.exe& goto input_params
if "%choice%"=="3" set exe=graph_cut_seam_carving.exe& goto input_params
if "%choice%"=="4" goto interactive_tool
if "%choice%"=="5" goto end
echo Invalid choice! Please try again.
timeout /t 2 >nul
goto menu

REM --- Section for standard 1, 2, 3 ---
:input_params
cls
echo ========================================
echo Selected: %exe%
echo ========================================
echo.

REM Check if images folder exists
if not exist "images" (
    mkdir images
    echo Created 'images' folder - please add your images there!
    pause
    goto menu
)

REM List available images
echo Available images in 'images' folder:
echo.
dir /b images\*.jpg images\*.jpeg images\*.png 2>nul
echo.

:get_input
set "input="
set /p input=Enter input image name (e.g., photo or photo.jpg): 
if "%input%"=="" (
    echo ERROR: Input name cannot be empty.
    goto :get_input
)
REM Your Python script will now find the file, so no 'if exist' check is needed.
echo.

:get_output
set "output="
set "full_output="
set /p output=Enter output image name (e.g., result): 
if "%output%"=="" (
    echo ERROR: Output name cannot be empty.
    goto :get_output
)

REM --- Add default .jpg extension ---
set "full_output=%output%"
set "ext="
for /f "tokens=2 delims=." %%a in ("%output%") do set "ext=%%a"
if "%ext%"=="" (
    set "full_output=%output%.jpg"
    echo (No extension provided. Saving as %full_output%)
)
echo.

:get_seams
set "seams="
set /p seams=Enter number of seams to remove (default 50): 
if "%seams%"=="" set seams=50

REM --- Robust validation for numbers ---
echo %seams% | findstr /R "^[1-9][0-9]*$" >nul
if errorlevel 1 (
    echo.
    echo ERROR: Input must be a positive number (e.g., 50).
    echo Please try again.
    echo.
    goto :get_seams
)
echo Seams: %seams%
echo.

:get_direction
set "direction="
set "dir_choice="
set /p dir_choice=Enter direction - (v)ertical or (h)orizontal (default v): 

if "%dir_choice%"=="" set "direction=vertical"
if /i "%dir_choice%"=="v" set "direction=vertical"
if /i "%dir_choice%"=="vertical" set "direction=vertical"
if /i "%dir_choice%"=="h" set "direction=horizontal"
if /i "%dir_choice%"=="horizontal" set "direction=horizontal"

if not defined direction (
    echo.
    echo ERROR: Invalid input. Please enter 'v' or 'h'.
    echo.
    goto :get_direction
)
echo Using direction: %direction%
echo.

REM --- This is your working bug fix ---
set viz_flag=
set visualize=n
REM Only ask for visualization if it's not the graph-cut exe
if not "%exe%"=="graph_cut_seam_carving.exe" (
    set "visualize="
    set /p visualize=Show step-by-step visualization? (y/n, default n): 
    echo (NOTE: This will pause on every seam)
    if /i "%visualize%"=="y" (
        set viz_flag=--visualize
        set visualize=y
    )
) else (
    set visualize=n (Not Supported)
)
REM --- End bug fix ---

echo.
echo ========================================
echo Running seam carving...
echo ========================================
echo Input: images\%input%
echo Output: images\%full_output%
echo Seams: %seams%
echo Direction: %direction%
echo Visualize: %visualize%
echo.

REM Run the program - This now passes the raw input name
%exe% "images\%input%" "images\%full_output%" --num_seams %seams% --direction %direction% %viz_flag%

REM --- This is your working error pause ---
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo  !!!   E R R O R   !!!
    echo ========================================
    echo The program ( %exe% ) failed.
    echo Please check the error message above.
    echo.
    pause
    goto menu
)
REM --- End error pause ---

echo.
echo ========================================
if exist "images\%full_output%" (
    echo SUCCESS! Output saved as: images\%full_output%
    echo.
    echo Creating comparison image...
    
    REM Run comparison viewer - Pass raw input name
    image_comparison_viewer.exe "images\%input%" "images\%full_output%" --save "images\comparison.jpg" --layout vertical
    
    if exist "images\comparison.jpg" (
        echo Comparison saved as: images\comparison.jpg
    )
) else (
    echo ERROR: Something went wrong!
    echo The file 'images\%full_output%' was not created.
    pause
)
echo ========================================
echo.
set "again="
set /p again=Process another image? (y/n): 
if /i "%again%"=="y" goto menu
goto end


REM --- Section for Interactive Tool ---
:interactive_tool
cls
echo ========================================
echo  Interactive Resizing Tool
echo ========================================
echo.
if not exist "images" (
    mkdir images
    echo Created 'images' folder - please add your images there!
    pause
    goto menu
)

echo Available images in 'images' folder:
echo.
dir /b images\*.jpg images\*.jpeg images\*.png 2>nul
echo.

:get_input_interactive
set "input="
set /p input=Enter input image name to open (e.g., photo or photo.jpg): 
if "%input%"=="" goto :get_input_interactive
REM Your Python script will handle finding the file.

echo.
echo Launching tool...
echo - Move the sliders to resize the image.
echo - (This may lag as it re-calculates!)
echo - Press 's' in the window to save the result.
echo - Press 'q' or ESC in the window to quit.
echo.

interactive_seam_carving.exe "images\%input%"

REM --- This is your working error pause ---
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo  !!!   E R R O R   !!!
    echo ========================================
    echo The interactive tool failed.
    echo Please check the error message above.
    echo.
    pause
)
REM --- End error pause ---

echo.
echo Tool closed.
pause
goto menu

:end
cls
echo Thank you for using Seam Carving Tool!
timeout /t 2 >nul
exit