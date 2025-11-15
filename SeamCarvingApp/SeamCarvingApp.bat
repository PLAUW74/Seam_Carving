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
echo 5. Exit
echo.
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

set /p input=Enter input image name (e.g., photo.jpg): 

REM Check if file exists
if not exist "images\%input%" (
    echo.
    echo ERROR: File "%input%" not found in 'images' folder!
    pause
    goto menu
)

set /p output=Enter output image name (e.g., result.jpg): 
set /p seams=Enter number of seams to remove (default 50): 
if "%seams%"=="" set seams=50

echo.
set /p direction=Enter direction - vertical or horizontal (default vertical): 
if "%direction%"=="" set direction=vertical

echo.
set /p visualize=Show step-by-step visualization? (y/n, default n): 
set viz_flag=
if /i "%visualize%"=="y" set viz_flag=--visualize

echo.
echo ========================================
echo Running seam carving...
echo ========================================
echo Input: images\%input%
echo Output: images\%output%
echo Seams: %seams%
echo Direction: %direction%
echo Visualize: %visualize%
echo.

REM Run the program
%exe% "images\%input%" "images\%output%" --num_seams %seams% --direction %direction% %viz_flag%

echo.
echo ========================================
if exist "images\%output%" (
    echo SUCCESS! Output saved as: images\%output%
    echo.
    echo Creating comparison image...
    
    REM Run comparison viewer
    image_comparison_viewer.exe "images\%input%" "images\%output%" --save "images\comparison.jpg" --layout vertical
    
    if exist "images\comparison.jpg" (
        echo Comparison saved as: images\comparison.jpg
    )
) else (
    echo ERROR: Something went wrong!
)
echo ========================================
echo.
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
set /p input=Enter input image name to open (e.g., photo.jpg): 

if not exist "images\%input%" (
    echo.
    echo ERROR: File "%input%" not found in 'images' folder!
    pause
    goto menu
)

echo.
echo Launching tool...
echo - Move the sliders to resize the image.
echo - Press 's' in the window to save the result.
echo - Press 'q' or ESC in the window to quit.
echo.

interactive_seam_carving.exe "images\%input%"

echo.
echo Tool closed.
pause
goto menu

:end
cls
echo Thank you for using Seam Carving Tool!
timeout /t 2 >nul
exit