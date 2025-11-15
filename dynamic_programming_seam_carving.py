# -*- coding: utf-8 -*-
"""Dynamic Programming Seam Carving
"""

import cv2
import numpy as np
import argparse
import sys
import time


def compute_energy(image):
    """
    Calculates the energy map of an image using the Sobel operator.
    The energy of a pixel is the sum of the absolute values of the
    gradients in the x and y directions.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # Compute energy map as the sum of absolute gradients
    energy_map = np.abs(sobel_x) + np.abs(sobel_y)

    return energy_map


def draw_seam(image, seam, direction):
    """
    Draws a seam (vertical or horizontal) on a copy of the image.
    """
    display_image = image.copy()
    if direction == 'vertical':
        for i in range(len(seam)):
            # Draw a red pixel at (row, col)
            display_image[i, seam[i]] = [0, 0, 255] # BGR for red
    else: # horizontal
        for j in range(len(seam)):
            # Draw a red pixel at (col, row)
            display_image[seam[j], j] = [0, 0, 255] # BGR for red
    return display_image


def find_vertical_seam_dp(energy_map):
    """
    Finds the lowest-energy vertical seam using dynamic programming.
    """
    height, width = energy_map.shape
    M = np.zeros_like(energy_map, dtype=np.float64)
    M[0, :] = energy_map[0, :]

    for i in range(1, height):
        for j in range(width):
            if j == 0:
                min_parent_energy = min(M[i - 1, j], M[i - 1, j + 1])
            elif j == width - 1:
                min_parent_energy = min(M[i - 1, j - 1], M[i - 1, j])
            else:
                min_parent_energy = min(
                    M[i - 1, j - 1], M[i - 1, j], M[i - 1, j + 1]
                )

            M[i, j] = energy_map[i, j] + min_parent_energy

    seam = np.zeros(height, dtype=np.uint32)
    j = np.argmin(M[-1, :])
    seam[-1] = j

    for i in range(height - 2, -1, -1):
        current_col = seam[i + 1]

        if current_col == 0:
            j = np.argmin(M[i, 0:2])
        elif current_col == width - 1:
            j = np.argmin(M[i, width - 2:width]) + (width - 2)
        else:
            j = (
                np.argmin(M[i, current_col - 1:current_col + 2])
                + (current_col - 1)
            )

        seam[i] = j

    return seam


def remove_vertical_seam(image, seam):
    """
    Removes a given vertical seam from an image.
    """
    height, width, channels = image.shape
    new_image = np.zeros((height, width - 1, channels), dtype=image.dtype)

    for i in range(height):
        col_to_remove = seam[i]
        new_image[i, :col_to_remove] = image[i, :col_to_remove]
        new_image[i, col_to_remove:] = image[i, col_to_remove + 1:]

    return new_image

def carve(image, num_seams, direction, visualize=False):
    """
    Repeatedly finds and removes seams from an image.
    'visualize=True' will show each seam before removal.
    """
    carved_image = np.copy(image)
    
    # Store the original for visualization
    original_for_viz = np.copy(image)

    for k in range(num_seams):
        
        # --- Visualization logic ---
        if visualize:
            # We must use the 'carved_image' for calculation
            # but we can show the seam on the 'original' for comparison
            # Note: This visualization isn't perfect, as seam coordinates
            # shift, but it's good for demonstration.
            # For a simpler viz, just use 'carved_image' in draw_seam.
            
            viz_img = np.copy(carved_image)
            
            # Find seam on the (potentially transposed) carved image
            if direction == "horizontal":
                energy_map = compute_energy(viz_img.transpose(1, 0, 2))
                seam = find_vertical_seam_dp(energy_map)
                
                # Draw on the *non-transposed* image
                viz_img = draw_seam(viz_img, seam, 'horizontal')

            else: # vertical
                energy_map = compute_energy(viz_img)
                seam = find_vertical_seam_dp(energy_map)
                
                # Draw on the image
                viz_img = draw_seam(viz_img, seam, 'vertical')
            
            print(f"Showing seam {k + 1}/{num_seams}. Press any key to continue...")
            cv2.imshow("Seam Visualization (press any key)", viz_img)
            cv2.waitKey(0) # Wait for a key press
        # --- End visualization logic ---


        # --- Carving logic ---
        
        # Transpose for horizontal seam removal
        if direction == "horizontal":
            carved_image = carved_image.transpose(1, 0, 2)

        # Compute energy map
        # If we visualized, we already have the energy_map and seam
        if not visualize:
            energy_map = compute_energy(carved_image)
            seam = find_vertical_seam_dp(energy_map)

        # Remove the seam
        carved_image = remove_vertical_seam(carved_image, seam)

        # Transpose back if horizontal
        if direction == "horizontal":
            carved_image = carved_image.transpose(1, 0, 2)

        # Print progress (use end='\r' to stay on one line)
        print(f"Removed seam {k + 1}/{num_seams}", end='\r')
    
    print("\nDone.") # Newline after loop
    
    # Clean up any open windows
    if visualize:
        cv2.destroyAllWindows()

    return carved_image


def main():
    parser = argparse.ArgumentParser(
        description="Dynamic Programming Seam Carving"
    )
    parser.add_argument(
        "input_image", type=str, help="Path to the input image"
    )
    parser.add_argument(
        "output_image", type=str, help="Path to save the carved image"
    )
    parser.add_argument(
        "--num_seams",
        type=int,
        default=50,
        help="Number of seams to remove",
    )
    parser.add_argument(
        "--direction",
        type=str,
        default="vertical",
        choices=["vertical", "horizontal"],
        help="Direction of seams to remove",
    )

    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Show each seam before removing it",
    )

    args = parser.parse_args()

    image = cv2.imread(args.input_image)
    if image is None:
        print(f"Error: Unable to read image from {args.input_image}")
        sys.exit(1)

    print(f"Original image size: {image.shape}")

    # record start time
    start = time.time()

    carved_image = carve(image, args.num_seams, args.direction, args.visualize)
    
    print(f"Carved image size: {carved_image.shape}")

    # record end time
    end = time.time()
    print(f"Time Taken: {end - start:.4f} seconds")

    cv2.imwrite(args.output_image, carved_image)
    print(f"Successfully saved carved image to {args.output_image}")


if __name__ == "__main__":
    main()
