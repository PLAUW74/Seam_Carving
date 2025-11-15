# -*- coding: utf-8 -*-
"""
Seam Carving using a Max-Flow / Min-Cut (Graph-Cut) Algorithm
Requires: numpy, opencv-python, scipy
"""

import cv2
import numpy as np
import argparse
import sys
import time
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import max_flow


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


def find_vertical_seam_graph_cut(energy_map):
    """
    Finds the lowest-energy vertical seam using a max-flow/min-cut
    formulation on a graph.
    """
    height, width = energy_map.shape
    
    # We use the node-splitting trick to give "nodes" (pixels) capacity
    # Total nodes = 2 (Source/Sink) + 2 * (height * width)
    # S = 0
    # T = 2 * height * width + 1
    # Pixel (i, j) -> in_node  = 1 + 2 * (i * width + j)
    # Pixel (i, j) -> out_node = 1 + 2 * (i * width + j) + 1
    
    num_nodes = 2 + 2 * height * width
    source = 0
    sink = 2 * height * width + 1
    
    # Use a COO (Coordinate) format to build the sparse graph quickly
    # (row, col) -> data
    graph_row = []
    graph_col = []
    graph_data = []
    
    inf = np.iinfo(np.int32).max

    # 1. Add edges from Source to top-row "in" nodes
    for j in range(width):
        in_node = 1 + 2 * (0 * width + j)
        graph_row.append(source)
        graph_col.append(in_node)
        graph_data.append(inf) # Infinite capacity

    # 2. Add edges from bottom-row "out" nodes to Sink
    for j in range(width):
        out_node = 1 + 2 * ((height - 1) * width + j) + 1
        graph_row.append(out_node)
        graph_col.append(sink)
        graph_data.append(inf) # Infinite capacity

    for i in range(height):
        for j in range(width):
            pixel_index = i * width + j
            in_node = 1 + 2 * pixel_index
            out_node = 1 + 2 * pixel_index + 1
            
            # 3. Add internal edges (pixel energy as capacity)
            # This is the edge that will be "cut"
            graph_row.append(in_node)
            graph_col.append(out_node)
            graph_data.append(energy_map[i, j])

            # 4. Add connectivity edges (out_node -> in_node of neighbors)
            if i < height - 1:
                # Check neighbors: (i+1, j-1), (i+1, j), (i+1, j+1)
                for dj in [-1, 0, 1]:
                    nj = j + dj
                    if 0 <= nj < width:
                        neighbor_index = (i + 1) * width + nj
                        neighbor_in_node = 1 + 2 * neighbor_index
                        
                        graph_row.append(out_node)
                        graph_col.append(neighbor_in_node)
                        graph_data.append(inf) # Infinite capacity
    
    # Create the sparse graph in CSR format (required by max_flow)
    capacity_matrix = csr_matrix((graph_data, (graph_row, graph_col)), 
                                 shape=(num_nodes, num_nodes))
    
    # --- Compute Max-Flow ---
    # This finds the min-cut. The result is a 'residual' graph.
    flow_result = max_flow(capacity_matrix, source, sink)
    residual_graph = flow_result.residual

    # --- Find the Seam ---
    # The seam is the set of "cut" edges. We can find this by
    # doing a Breadth-First Search (BFS) from the source on the
    # residual graph. All nodes reachable from S are on the 'S' side.
    # Any node (i,j) where in_node is reachable but out_node is not
    # is part of the min-cut (i.e., the seam).
    
    seam = np.zeros(height, dtype=np.uint32)
    
    # Find all nodes reachable from source
    reachable = np.zeros(num_nodes, dtype=bool)
    q = [source]
    reachable[source] = True
    
    while q:
        u = q.pop(0)
        # Find neighbors in the residual graph
        # nonzero returns (row_indices, col_indices)
        neighbors = residual_graph[u].nonzero()[1]
        for v in neighbors:
            if not reachable[v]:
                reachable[v] = True
                q.append(v)
                
    # Check for cut edges (in_node is reachable, out_node is not)
    for i in range(height):
        for j in range(width):
            pixel_index = i * width + j
            in_node = 1 + 2 * pixel_index
            out_node = 1 + 2 * pixel_index + 1
            
            if reachable[in_node] and not reachable[out_node]:
                seam[i] = j
                # We assume only one pixel per row is in the seam
                break
                
    return seam


# --- Carve function (uses the new find_seam) ---
def carve(image, num_seams, direction):
    carved_image = np.copy(image)

    for k in range(num_seams):
        if direction == "horizontal":
            carved_image = carved_image.transpose(1, 0, 2)

        energy_map = compute_energy(carved_image)
        
        # --- Use the new Graph-Cut function ---
        seam = find_vertical_seam_graph_cut(energy_map)
        
        carved_image = remove_vertical_seam(carved_image, seam)

        if direction == "horizontal":
            carved_image = carved_image.transpose(1, 0, 2)

        print(f"Removed seam {k + 1}/{num_seams} (Graph-Cut)")

    return carved_image


def main():
    parser = argparse.ArgumentParser(
        description="Graph-Cut Seam Carving (Max-Flow)"
    )
    # ... (Add the same argparse arguments as your other scripts) ...
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
    start = time.time()
    
    carved_image = carve(image, args.num_seams, args.direction)
    
    print(f"Carved image size: {carved_image.shape}")
    end = time.time()
    print(f"Time Taken: {end - start:.4f} seconds")

    cv2.imwrite(args.output_image, carved_image)
    print(f"Successfully saved carved image to {args.output_image}")


if __name__ == "__main__":
    main()