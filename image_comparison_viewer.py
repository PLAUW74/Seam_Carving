# -*- coding: utf-8 -*-
"""Image Comparison Viewer - Compare original and carved images"""

import cv2
import numpy as np
import argparse
import sys
import os


def create_comparison_image(input_path, output_path, layout='vertical'):
    """
    Creates a comparison image showing input above and output below
    (or side-by-side).

    Args:
        input_path: Path to the original/input image
        output_path: Path to the carved/output image
        layout: 'vertical' (stacked) or 'horizontal' (side-by-side)

    Returns:
        Combined comparison image
    """
    # Read both images
    input_img = cv2.imread(input_path)
    output_img = cv2.imread(output_path)

    if input_img is None:
        print(f"Error: Unable to read input image from {input_path}")
        sys.exit(1)

    if output_img is None:
        print(f"Error: Unable to read output image from {output_path}")
        sys.exit(1)

    # Get dimensions
    input_h, input_w = input_img.shape[:2]
    output_h, output_w = output_img.shape[:2]

    # Add labels to images
    input_labeled = add_label(
        input_img.copy(), f"Original ({input_w}x{input_h})"
    )
    output_labeled = add_label(
        output_img.copy(), f"Carved ({output_w}x{output_h})"
    )

    if layout == 'vertical':
        # Stack vertically (input above, output below)
        # Make both images the same width for clean stacking
        max_width = max(input_w, output_w)

        # Resize if needed to match widths
        if input_w != max_width:
            scale = max_width / input_w
            new_h = int(input_h * scale)
            input_labeled = cv2.resize(input_labeled, (max_width, new_h))

        if output_w != max_width:
            scale = max_width / output_w
            new_h = int(output_h * scale)
            output_labeled = cv2.resize(output_labeled, (max_width, new_h))

        # Add separator line
        separator = np.ones((5, max_width, 3), dtype=np.uint8) * 255

        # Stack images
        comparison = np.vstack([input_labeled, separator, output_labeled])

    else:  # horizontal layout
        # Place side-by-side
        # Make both images the same height for clean alignment
        max_height = max(input_h, output_h)

        # Resize if needed to match heights
        if input_h != max_height:
            scale = max_height / input_h
            new_w = int(input_w * scale)
            input_labeled = cv2.resize(input_labeled, (new_w, max_height))

        if output_h != max_height:
            scale = max_height / output_h
            new_w = int(output_w * scale)
            output_labeled = cv2.resize(output_labeled, (new_w, max_height))

        # Add separator line
        separator = np.ones((max_height, 5, 3), dtype=np.uint8) * 255

        # Stack images horizontally
        comparison = np.hstack([input_labeled, separator, output_labeled])

    return comparison


def add_label(image, text):
    """Adds a text label at the top of an image."""
    # Create a white bar at the top for the label
    label_height = 40
    h, w = image.shape[:2]

    # Create white background for label
    label_bar = np.ones((label_height, w, 3), dtype=np.uint8) * 255

    # Add text to label bar
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    thickness = 2

    # Get text size to center it
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = (w - text_w) // 2
    text_y = (label_height + text_h) // 2

    cv2.putText(label_bar, text, (text_x, text_y), font, font_scale,
                (0, 0, 0), thickness, cv2.LINE_AA)

    # Combine label bar with image
    labeled_image = np.vstack([label_bar, image])

    return labeled_image


def main():
    parser = argparse.ArgumentParser(
        description='Compare original and seam-carved images'
    )
    parser.add_argument(
        'input_image', type=str, help='Path to the original/input image'
    )
    parser.add_argument(
        'output_image', type=str, help='Path to the carved/output image'
    )
    parser.add_argument(
        '--layout',
        type=str,
        default='vertical',
        choices=['vertical', 'horizontal'],
        help='Layout: vertical (stacked) or horizontal (side-by-side)'
    )
    parser.add_argument(
        '--save',
        type=str,
        default='comparison.jpg',
        help='Path to save the comparison image'
    )
    parser.add_argument(
        '--display',
        action='store_true',
        help='Display the comparison in a window (press any key to close)'
    )

    args = parser.parse_args()

    print("Creating comparison image...")
    print(f"Input: {args.input_image}")
    print(f"Output: {args.output_image}")
    print(f"Layout: {args.layout}")

    # Create comparison
    comparison = create_comparison_image(
        args.input_image,
        args.output_image,
        args.layout
    )

    # Save comparison image
    save_path = args.save

    # Ensure the path has a valid extension
    if not save_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        save_path += '.jpg'

    # Debug info
    print(f"Attempting to save to: {save_path}")
    print(f"Absolute path: {os.path.abspath(save_path)}")

    # Try to save
    success = cv2.imwrite(save_path, comparison)

    if success:
        print(f"Comparison saved to: {save_path}")
    else:
        print("ERROR: Failed to save comparison image!")
        print("Check if the directory exists and you have write "
              "permissions.")
        sys.exit(1)

    # Display if requested
    if args.display:
        # Resize if image is too large for screen
        h, w = comparison.shape[:2]
        max_dimension = 1200

        if h > max_dimension or w > max_dimension:
            scale = max_dimension / max(h, w)
            new_w = int(w * scale)
            new_h = int(h * scale)
            comparison_display = cv2.resize(comparison, (new_w, new_h))
        else:
            comparison_display = comparison

        window_title = 'Image Comparison (Press any key to close)'
        cv2.imshow(window_title, comparison_display)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print("Done!")


if __name__ == "__main__":
    main()
