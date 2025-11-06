# -*- coding: utf-8 -*-
"""Dynamic Programming Seam Carving
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
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # Compute energy map as the sum of absolute gradients
    energy_map = np.abs(sobel_x) + np.abs(sobel_y)

    return energy_map


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


def carve(image, num_seams, direction):
    """
    Repeatedly finds and removes seams from an image.
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

        print(f"Removed seam {k + 1}/{num_seams} (DP)")

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

    args = parser.parse_args()

    image = cv2.imread(args.input_image)
    if image is None:
        print(f"Error: Unable to read image from {args.input_image}")
        sys.exit(1)

    print(f"Original image size: {image.shape}")

    carved_image = carve(image, args.num_seams, args.direction)

    print(f"Carved image size: {carved_image.shape}")

    cv2.imwrite(args.output_image, carved_image)
    print(f"Successfully saved carved image to {args.output_image}")


if __name__ == "__main__":
    main()
