@echo off
title Seam Carving Tool
color 0A

:menu
cls
echo ========================================
echo       SEAM CARVING TOOL
echo ========================================
echo.
echo Place your images in the 'images' folder first!
echo.
echo Choose an algorithm:
echo.
echo 1. Dynamic Programming (Better Quality, Slower)
echo 2. Greedy Algorithm (Faster, Lower Quality)
echo 3. Exit
echo.
set /p choice=Enter your choice (1-3): 

if "%choice%"=="1" goto dp_algorithm
if "%choice%"=="2" goto greedy_algorithm
if "%choice%"=="3" goto end
echo Invalid choice! Please try again.
timeout /t 2 >nul
goto menu

:dp_algorithm
set exe=dynamic_programming_seam_carving.exe
goto input_params

:greedy_algorithm
set exe=greedy_algorithm_seam_carving.exe
goto input_params

:input_params
cls
echo ========================================
echo Selected: %exe%
echo ========================================
echo.

REM Check if images folder exists, create if not
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

REM Check if file exists in images folder
if not exist "images\%input%" (
    echo.
    echo ERROR: File "%input%" not found in 'images' folder!
    echo Please make sure the image is in the 'images' folder.
    pause
    goto menu
)

set /p output=Enter output image name (e.g., result.jpg): 
set /p seams=Enter number of seams to remove (default 50): 

REM Set default value if empty
if "%seams%"=="" set seams=50

echo.
set /p direction=Enter direction - vertical or horizontal (default vertical): 
if "%direction%"=="" set direction=vertical

echo.
echo ========================================
echo Running seam carving...
echo ========================================
echo Input: images\%input%
echo Output: images\%output%
echo Seams: %seams%
echo Direction: %direction%
echo.

REM Run the program with images folder paths
%exe% "images\%input%" "images\%output%" --num_seams %seams% --direction %direction%

echo.
echo ========================================
if exist "images\%output%" (
    echo SUCCESS! Output saved as: images\%output%
    echo.
    echo Creating comparison image...
    
    REM Run comparison viewer - always save as comparison.jpg
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

:end
cls
echo Thank you for using Seam Carving Tool!
timeout /t 2 >nul
exit