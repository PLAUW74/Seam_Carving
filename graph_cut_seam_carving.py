# -*- coding: utf-8 -*-
"""
Seam Carving using a Graph (Shortest Path Algorithm)
This is an alternative to the Max-Flow / Min-Cut approach, which
is unstable when compiled. This version uses Dijkstra's algorithm
on a sparse graph, which is equivalent and more stable.
"""

import cv2
import numpy as np
import argparse
import sys
import time
import os
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

# --- Energy function (same as before) ---
def compute_energy(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    return np.abs(sobel_x) + np.abs(sobel_y)


# --- Seam removal (same as before) ---
def remove_vertical_seam(image, seam):
    height, width, channels = image.shape
    new_image = np.zeros((height, width - 1, channels), dtype=image.dtype)
    for i in range(height):
        col_to_remove = seam[i]
        new_image[i, :col_to_remove] = image[i, :col_to_remove]
        new_image[i, col_to_remove:] = image[i, col_to_remove + 1:]
    return new_image


def find_vertical_seam_shortest_path(energy_map):
    """
    Finds the lowest-energy vertical seam by building a graph and
    finding the shortest path from a virtual 'source' to 'sink'.
    """
    height, width = energy_map.shape
    
    # Total nodes = (height * width) + 2 virtual nodes
    num_nodes = height * width + 2
    source_node = height * width
    sink_node = height * width + 1
    
    # Helper to map (row, col) to a node index
    def pixel_to_node(i, j):
        return i * width + j

    # We build the sparse graph in COO format (row, col, data)
    graph_rows = []
    graph_cols = []
    graph_data = []

    # 1. Connect Source to all top-row pixels
    for j in range(width):
        graph_rows.append(source_node)
        graph_cols.append(pixel_to_node(0, j))
        graph_data.append(energy_map[0, j])

    # 2. Connect all other pixels to their 3 children
    for i in range(height - 1):
        for j in range(width):
            current_node = pixel_to_node(i, j)
            # Check neighbors: (i+1, j-1), (i+1, j), (i+1, j+1)
            for dj in [-1, 0, 1]:
                nj = j + dj
                if 0 <= nj < width:
                    neighbor_node = pixel_to_node(i + 1, nj)
                    graph_rows.append(current_node)
                    graph_cols.append(neighbor_node)
                    graph_data.append(energy_map[i + 1, nj])

    # 3. Connect all bottom-row pixels to the Sink
    for j in range(width):
        graph_rows.append(pixel_to_node(height - 1, j))
        graph_cols.append(sink_node)
        graph_data.append(0) # No cost to go to sink
    
    # Create the sparse graph
    graph = csr_matrix((graph_data, (graph_rows, graph_cols)), 
                       shape=(num_nodes, num_nodes))
    
    # --- Compute Shortest Path ---
    # Find shortest path from 'source_node' to all other nodes
    distances, predecessors = shortest_path(
        csgraph=graph,
        directed=True,
        indices=source_node,
        return_predecessors=True
    )

    # The shortest path to the sink is our seam energy, but we
    # need to find the *end* of the seam by finding the
    # bottom-row pixel that connects to the sink with the min cost.
    
    # Find the node in the last row with the min total distance
    min_dist = np.inf
    end_node = -1
    for j in range(width):
        node = pixel_to_node(height - 1, j)
        if distances[node] < min_dist:
            min_dist = distances[node]
            end_node = node
            
    if end_node == -1:
        # This should not happen, but as a fallback, take the min energy
        end_node = pixel_to_node(height - 1, np.argmin(energy_map[height - 1]))

    # --- Backtrack from the end node to find the seam ---
    seam = np.zeros(height, dtype=np.uint32)
    current_node = end_node
    
    for i in range(height - 1, -1, -1):
        if current_node == -9999 or current_node == source_node:
            # We've reached the start, but something is wrong
            # As a fallback, just use the current column
            print("Warning: Shortest path backtrack failed. Using fallback.")
            seam[i] = seam[i+1] if i < height - 1 else 0
        else:
            seam[i] = current_node % width # Get col from node index
            current_node = predecessors[current_node]

    return seam


# --- Carve function (uses the new find_seam) ---
def carve(image, num_seams, direction):
    carved_image = np.copy(image)

    for k in range(num_seams):
        if direction == "horizontal":
            carved_image = carved_image.transpose(1, 0, 2)

        energy_map = compute_energy(carved_image)
        
        # --- Use the new Shortest Path function ---
        seam = find_vertical_seam_shortest_path(energy_map)
        
        carved_image = remove_vertical_seam(carved_image, seam)

        if direction == "horizontal":
            carved_image = carved_image.transpose(1, 0, 2)

        print(f"Removed seam {k + 1}/{num_seams} (Graph-Shortest-Path)", end='\r')
    
    print("\nDone.") # Newline after loop
    return carved_image


def find_image_path(input_path):
    """
    Finds a valid image path.
    If 'input_path' is not found, it tries appending
    .jpg, .jpeg, and .png.
    """
    if os.path.exists(input_path):
        return input_path

    # Check for other extensions
    for ext in ['.jpg', 'jpeg', '.png']:
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


def main():
    parser = argparse.ArgumentParser(
        description="Graph-Based Seam Carving (Shortest Path)"
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

    input_image_path = find_image_path(args.input_image)

    if input_image_path is None:
        print(f"Error: Unable to find image file for '{args.input_image}'")
        sys.exit(1)

    image = cv2.imread(input_image_path)
    
    if image is None:
        print(f"Error: Unable to read image from {args.input_image}")
        sys.exit(1)

    print(f"Original image size: {image.shape}")
    start = time.time()
    
    carved_image = carve(image, args.num_seams, args.direction)
    
    print(f"Carved image size: {carved_image.shape}")
    end = time.time()
    print(f"Time Taken: {end - start:.4f} seconds")

    cv2.imwrite(args.output_image, carved_image)
    print(f"Successfully saved carved image to {args.output_image}")


if __name__ == "__main__":
    main()