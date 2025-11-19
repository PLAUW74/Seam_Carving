# Seam Carving Implementation

This project implements content-aware image resizing using seam carving algorithms. It provides a fully portable, compiled application for Windows.

## Overview

Seam carving is an algorithm for content-aware image resizing that removes low-energy seams (paths of pixels) from an image to reduce its size while preserving important content. This implementation provides three distinct approaches:

- **Dynamic Programming Algorithm**: Optimal seam removal using dynamic programming.
- **Greedy Algorithm**: Faster approximation using greedy selection.
- **Graph-Based Algorithm**: Uses Dijkstra's Shortest Path algorithm on a sparse graph (Bonus Implementation).

## Features

- **Standalone Executables**: No Python installation required for the end-user; runs via compiled `.exe` files.
- **Portable Build System**: Includes a self-contained Python environment for building the project.
- **Interactive Tool**: Real-time resizing with a pre-computed cache for instant performance.
- **Comparison Viewer**: Automatically generates side-by-side comparisons of original vs. carved images.

## Prerequisites

- **Windows 10 or 11**
- *Note: Python is NOT required to be installed on your system. This repository includes a portable Python environment for building and running.*

## Seam Carving Application & File Structure

### How To Use
1. Navigate to the `SeamCarvingApp` folder.
2. Refer to `HOW_TO_USE.txt` for detailed instructions.
3. Run `SeamCarvingApp.exe` to start the tool.

### How to Build
If you have modified the source code and need to rebuild the executables:
1. Navigate to the root folder.
2. Refer to `HOW_TO_BUILD.txt`.
3. Run `ALL_SETUP.bat`.