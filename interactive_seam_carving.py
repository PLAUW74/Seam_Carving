# -*- coding: utf-8 -*-
"""
Interactive Seam Carving Tool using OpenCV Trackbars
"""

import cv2
import numpy as np
import sys
import argparse

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


# --- We need a modified carve function that works on a copy ---
# This is slightly different from the one in the main script
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

def on_trackbar_change(val):
    """
    Callback function for when a slider is moved.
    """
    global original_image, current_image, window_name
    
    # Get current slider positions
    target_width_seams = cv2.getTrackbarPos("Width", window_name)
    target_height_seams = cv2.getTrackbarPos("Height", window_name)
    
    h, w = original_image.shape[:2]
    
    # Calculate how many seams to remove
    seams_to_remove_v = w - target_width_seams
    seams_to_remove_h = h - target_height_seams
    
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
    # Create a blank canvas to show the image (in case size is small)
    display_h, display_w = original_image.shape[:2]
    display_canvas = np.zeros((display_h, display_w, 3), dtype=np.uint8)
    
    # Copy the carved image onto the canvas
    final_h, final_w = current_image.shape[:2]
    display_canvas[0:final_h, 0:final_w] = current_image
    
    cv2.imshow(window_name, display_canvas)


def main():
    global original_image, current_image, window_name
    
    parser = argparse.ArgumentParser(
        description="Interactive Seam Carving Tool"
    )
    parser.add_argument(
        "input_image", type=str, help="Path to the input image"
    )
    args = parser.parse_args()

    original_image = cv2.imread(args.input_image)
    if original_image is None:
        print(f"Error: Unable to read image from {args.input_image}")
        sys.exit(1)
        
    current_image = original_image.copy()
    
    h, w = original_image.shape[:2]

    # Create a window
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    # Create trackbars
    # The 'on_trackbar_change' function is called *only* when the slider is moved
    cv2.createTrackbar("Width", window_name, w, w, on_trackbar_change)
    cv2.createTrackbar("Height", window_name, h, h, on_trackbar_change)
    
    # Set min values for trackbars
    cv2.setTrackbarMin("Width", window_name, 1)
    cv2.setTrackbarMin("Height", window_name, 1)

    print("--- Interactive Seam Carving ---")
    print("Move the sliders to resize the image.")
    print("Press 's' to save the current result.")
    print("Press 'q' or ESC to quit.")

    # Show the initial image (on a canvas)
    display_canvas = np.zeros((h, w, 3), dtype=np.uint8)
    display_canvas[0:h, 0:w] = current_image
    cv2.imshow(window_name, display_canvas)

    while True:
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord('q') or key == 27: # 'q' or ESC
            break
        elif key == ord('s'):
            save_path = "interactive_result.jpg"
            cv2.imwrite(save_path, current_image)
            print(f"\nImage saved to {save_path}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()