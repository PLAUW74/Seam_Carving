# Seam Carving Application & File Structure

Quick Start Guide
- Find the folder "SeamCarving Application", refer to HOWTOUSE.txt to run the application.

Source Files are:
- dynamic_programming_seam_carving.py (Dynamic Programming)
- greedy_algorithm_seam_carving.py (Greedy Method)
- image_comparison_viewer.py

Bonus:
- CI/CD (using Github Actions, refer to /.github/workflows/ci-cd.yml)



# Seam Carving Implementation (IF YOU WANT TO BUILD FROM SCRATCH)

This project implements content-aware image resizing using seam carving algorithms, including both dynamic programming and greedy approaches.

## Overview

Seam carving is an algorithm for content-aware image resizing that removes low-energy seams (paths of pixels) from an image to reduce its size while preserving important content. This implementation provides two algorithms:

- **Dynamic Programming Algorithm**: Optimal seam removal using dynamic programming
- **Greedy Algorithm**: Faster approximation using greedy selection

## Prerequisites

- Python 3.x
- pip package manager

## Installation

### 1. Set Up Virtual Environment (Recommended)

Using a virtual environment helps manage dependencies and avoid conflicts.
Virtual environment just a folder to store the python dependencies. Like a "Local Library of header files"

#### On macOS/Linux:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (WSL)
source venv/bin/activate
```

#### On Windows: (cmd line)
```bash
# Create virtual environment
python -m venv <Location>

# Activate virtual environment
<Location>\venv\Scripts\activate.bat
```

### 2. Install Dependencies
```bash
pip install numpy opencv-python
```

## Usage

Both scripts accept command-line arguments to specify input/output files, carving direction, and the number of seams to remove.

### Dynamic Programming Algorithm

**Basic syntax:**
```bash
python dynamic_programming_seam_carving.py <input_image> <output_image> --direction=<vertical|horizontal> --num_seams=<number>
```

**Examples:**

Remove 50 vertical seams:
```bash
python dynamic_programming_seam_carving.py input.jpg output_dp.jpg --direction=vertical --num_seams=50
```

Remove 100 horizontal seams:
```bash
python dynamic_programming_seam_carving.py input.jpg output_dp_h.jpg --direction=horizontal --num_seams=100
```

### Greedy Algorithm

**Basic syntax:**
```bash
python greedy_algorithm_seam_carving.py <input_image> <output_image> --direction=<vertical|horizontal> --num_seams=<number>
```

**Example:**

Remove 50 vertical seams:
```bash
python greedy_algorithm_seam_carving.py input.jpg output_greedy.jpg --direction=vertical --num_seams=50
```

## Command-Line Arguments

| Argument | Description | Options |
|----------|-------------|---------|
| `input_image` | Path to the input image file | Any valid image file path |
| `output_image` | Path to save the processed image | Desired output file path |
| `--direction` | Direction of seam removal | `vertical` or `horizontal` |
| `--num_seams` | Number of seams to remove | Positive integer |

## Algorithm Comparison

- **Dynamic Programming**: Provides optimal seam selection but may be slower for large images
- **Greedy**: Faster execution with approximate results, suitable for quick previews or less critical applications

## Notes

- Vertical seams reduce image width
- Horizontal seams reduce image height
- The number of seams should not exceed the corresponding image dimension
- Processing time increases with image size and number of seams