# -*- coding: utf-8 -*-
"""Greedy Algorithm Seam Carving
"""

import cv2
import numpy as np
import argparse
import sys

def compute_energy(image):
    """
    Calculates the energy map of an image using the Sobel operator.
    The energy of a pixel is the sum of the absolute values of the
    gradients in the x and y directions.
    (Identical to the DP version)
    """
    # Convert image to grayscale for energy calculation
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute gradients in x and y directions using Sobel filter
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # Compute the energy map as the sum of absolute gradients
    energy_map = np.abs(sobel_x) + np.abs(sobel_y)

    return energy_map

def find_vertical_seam_greedy(energy_map):
    """
    Finds a vertical seam using a greedy algorithm.
    At each row, it simply picks the pixel with the lowest energy
    from the 3-pixel neighborhood below the current pixel.
    """
    height, width = energy_map.shape
    seam = np.zeros(height, dtype=np.uint32)

    # Find the start of the seam in the first row (pixel with min energy)
    current_col = np.argmin(energy_map[0, :])
    seam[0] = current_col

    # Iterate from the second row down to the last
    for i in range(1, height):
        # Define the 3-pixel neighborhood to check in the current row
        # This is centered around the column from the previous row

        # Handle left boundary
        if current_col == 0:
            neighborhood = energy_map[i, 0:2] # Check col 0, 1
            min_index_in_neighborhood = np.argmin(neighborhood)
            current_col = min_index_in_neighborhood # new col will be 0 or 1

        # Handle right boundary
        elif current_col == width - 1:
            neighborhood = energy_map[i, width-2:width] # Check col w-2, w-1
            min_index_in_neighborhood = np.argmin(neighborhood)
            current_col = (width - 2) + min_index_in_neighborhood # new col will be w-2 or w-1

        # General case
        else:
            neighborhood = energy_map[i, current_col-1:current_col+2] # Check col-1, col, col+1
            min_index_in_neighborhood = np.argmin(neighborhood)
            current_col = (current_col - 1) + min_index_in_neighborhood # new col will be col-1, col, or col+1

        seam[i] = current_col

    return seam

def remove_vertical_seam(image, seam):
    """
    Removes a given vertical seam from an image.
    (Identical to the DP version)
    """
    height, width, channels = image.shape

    # Create a new image with width-1
    new_image = np.zeros((height, width - 1, channels), dtype=image.dtype)

    # Iterate over each row and reconstruct the image without the seam pixel
    for i in range(height):
        col_to_remove = seam[i]

        # Copy pixels to the left of the seam
        new_image[i, :col_to_remove] = image[i, :col_to_remove]

        # Copy pixels to the right of the seam
        new_image[i, col_to_remove:] = image[i, col_to_remove+1:]

    return new_image

def carve(image, num_seams, direction):
    """
    Repeatedly finds and removes seams from an image.
    """
    # Make a copy to avoid modifying the original
    carved_image = np.copy(image)

    for k in range(num_seams):
        # Transpose the image to remove horizontal seams
        if direction == 'horizontal':
            carved_image = carved_image.transpose(1, 0, 2)

        # 1. Compute the energy map
        energy_map = compute_energy(carved_image)

        # 2. Find the minimum vertical seam using the GREEDY method
        seam = find_vertical_seam_greedy(energy_map)

        # 3. Remove the seam
        carved_image = remove_vertical_seam(carved_image, seam)

        # Transpose back if we were removing a horizontal seam
        if direction == 'horizontal':
            carved_image = carved_image.transpose(1, 0, 2)

        # Optional: Print progress
        print(f"Removed seam {k+1}/{num_seams} (Greedy)")

    return carved_image

def main():
    parser = argparse.ArgumentParser(description='Greedy Algorithm Seam Carving')
    parser.add_argument('input_image', type=str, help='Path to the input image')
    parser.add_argument('output_image', type=str, help='Path to save the carved image')
    parser.add_argument('--num_seams', type=int, default=50, help='Number of seams to remove')
    parser.add_argument('--direction', type=str, default='vertical', choices=['vertical', 'horizontal'], help='Direction of seams to remove')

    args = parser.parse_args()

    # Read the image
    image = cv2.imread(args.input_image)
    if image is None:
        print(f"Error: Unable to read image from {args.input_imge}")
        sys.exit(1)

    print(f"Original image size: {image.shape}")

    # Perform seam carving
    carved_image = carve(image, args.num_seams, args.direction)

    print(f"Carved image size: {carved_image.shape}")

    # Save the result
    cv2.imwrite(args.output_image, carved_image)
    print(f"Successfully saved carved image to {args.output_image}")

if __name__ == '__main__':
    main()