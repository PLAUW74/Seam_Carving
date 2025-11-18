# -*- coding: utf-8 -*-
"""
Interactive Seam Carving Tool using OpenCV Trackbars
(Modified for performance and stability)
"""

import cv2
import numpy as np
import sys
import argparse
import os

# --- Import functions from your existing DP script ---
try:
    from dynamic_programming_seam_carving import (
        compute_energy, 
        find_vertical_seam_dp, 
        remove_vertical_seam
    )
except ImportError:
    print("Error: Could not find 'dynamic_programming_seam_carving.py'")
    print("Please make sure this script is in the same folder.")
    sys.exit(1)


def find_image_path(input_path):
    """
    Finds a valid image path.
    If 'input_path' is not found, it tries appending
    .jpg, .jpeg, and .png.
    """
    if os.path.exists(input_path):
        return input_path

    # Check for other extensions
    for ext in ['.jpg', '.jpeg', '.png']:
        path_with_ext = input_path + ext
        if os.path.exists(path_with_ext):
            print(f"Input '{input_path}' not found, using '{path_with_ext}'")
            return path_with_ext

    # Check if user already included extension but file is missing
    base, ext = os.path.splitext(input_path)
    if ext in ['.jpg', '.jpeg', '.png']:
         if os.path.exists(base):
            print(f"Input '{input_path}' not found, using '{base}'")
            return base

    return None

# --- We need a modified carve function that works on a copy ---
def carve(image, num_seams, direction):
    """
    Carves an image. This version is simplified for the
    interactive tool and doesn't have visualization.
    """
    carved_image = np.copy(image)

    for k in range(num_seams):
        if direction == "horizontal":
            carved_image = carved_image.transpose(1, 0, 2)

        energy_map = compute_energy(carved_image)
        seam = find_vertical_seam_dp(energy_map)
        carved_image = remove_vertical_seam(carved_image, seam)

        if direction == "horizontal":
            carved_image = carved_image.transpose(1, 0, 2)
        
        # Update progress in the console
        print(f"Removing {direction} seam {k + 1}/{num_seams}   ", end='\r')

    return carved_image

# --- Global variables to store image and state ---
original_image = None
current_image = None
window_name = "Interactive Seam Carving"
TRACKBARS_INITIALIZED = False

def update_image():
    """
    Callback function for when sliders have changed.
    """
    global original_image, current_image, window_name, TRACKBARS_INITIALIZED

    if not TRACKBARS_INITIALIZED:
        return
    
    # Get current slider positions
    target_width_seams = cv2.getTrackbarPos("Width", window_name)
    target_height_seams = cv2.getTrackbarPos("Height", window_name)
    
    h, w = original_image.shape[:2]
    
    # Calculate how many seams to remove
    seams_to_remove_v = w - target_width_seams
    seams_to_remove_h = h - target_height_seams
    
    # Check if a change is actually needed
    if seams_to_remove_v == 0 and seams_to_remove_h == 0:
        current_image = original_image.copy() # Reset to original
    else:
        print("\n--- New Request ---")
        print(f"Target size: {target_width_seams}w x {target_height_seams}h")
        
        # Start from a fresh copy of the original image
        temp_image = np.copy(original_image)
        
        # 1. Carve Vertically (Width)
        if seams_to_remove_v > 0:
            print(f"Removing {seams_to_remove_v} vertical seams...")
            temp_image = carve(temp_image, seams_to_remove_v, "vertical")
        
        # 2. Carve Horizontally (Height)
        if seams_to_remove_h > 0:
            print(f"Removing {seams_to_remove_h} horizontal seams...")
            temp_image = carve(temp_image, seams_to_remove_h, "horizontal")
            
        print("\nUpdate complete.")
        
        # Update the global current image
        current_image = temp_image
    
    # --- Display the final image ---
    display_h, display_w = original_image.shape[:2]
    display_canvas = np.zeros((display_h, display_w, 3), dtype=np.uint8)
    
    # Copy the carved image onto the canvas
    final_h, final_w = current_image.shape[:2]
    display_canvas[0:final_h, 0:final_w] = current_image
    
    cv2.imshow(window_name, display_canvas)


def main():
    global original_image, current_image, window_name, TRACKBARS_INITIALIZED
    
    parser = argparse.ArgumentParser(
        description="Interactive Seam Carving Tool"
    )
    parser.add_argument(
        "input_image", type=str, help="Path to the input image"
    )
    args = parser.parse_args()

    input_image_path = find_image_path(args.input_image)

    if input_image_path is None:
        print(f"Error: Unable to find image file for '{args.input_image}'")
        sys.exit(1)

    original_image = cv2.imread(input_image_path)
    
    if original_image is None:
        print(f"Error: Unable to read image from {args.input_image}")
        sys.exit(1)
        
    current_image = original_image.copy()
    
    h, w = original_image.shape[:2]

    # Create a window
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    # Create trackbars with a DUMMY callback
    cv2.createTrackbar("Width", window_name, w, w, lambda x: None)
    cv2.createTrackbar("Height", window_name, h, h, lambda x: None)
    
    # Set min values for trackbars
    cv2.setTrackbarMin("Width", window_name, 1)
    cv2.setTrackbarMin("Height", window_name, 1)

    print("--- Interactive Seam Carving ---")
    print("Move the sliders to resize the image.")
    print("The image will update when you release the slider.")
    print("Press 's' to save the current result.")
    print("Press 'q' or ESC to quit.")

    # Show the initial image
    display_canvas = np.zeros((h, w, 3), dtype=np.uint8)
    display_canvas[0:h, 0:w] = current_image
    cv2.imshow(window_name, display_canvas)

    TRACKBARS_INITIALIZED = True

    last_w = w
    last_h = h
    
    while True:
        key = cv2.waitKey(50) & 0xFF
        
        current_w = cv2.getTrackbarPos("Width", window_name)
        current_h = cv2.getTrackbarPos("Height", window_name)
        
        if current_w != last_w or current_h != last_h:
            print("Slider change detected, running update...")
            update_image()
            last_w = current_w
            last_h = current_h
        
        if key == ord('q') or key == 27: # 'q' or ESC
            break
        elif key == ord('s'):
            # --- THIS IS THE MODIFIED BLOCK ---
            images_dir = "images"
            save_path = os.path.join(images_dir, "interactive_result.jpg")
            
            # Ensure the 'images' directory exists
            try:
                os.makedirs(images_dir, exist_ok=True)
            except OSError as e:
                print(f"\nError creating directory {images_dir}: {e}")
                continue # Skip saving

            cv2.imwrite(save_path, current_image)
            print(f"\nImage saved to {save_path}")
            # --- END OF MODIFIED BLOCK ---

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()