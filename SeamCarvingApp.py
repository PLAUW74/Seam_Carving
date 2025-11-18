# -*- coding: utf-8 -*-
"""
Seam Carving Application Launcher
This script replaces SeamCarvingApp.bat to provide a stable
Python-based menu for running the compiled .exe tools.
"""

import os
import sys

# --- Helper to check for images folder ---
def check_images_folder():
    if not os.path.exists("images"):
        print("Creating 'images' folder - please add your images there!")
        os.makedirs("images")
        
    print("Available images in 'images' folder:")
    print("-" * 30)
    
    files = [f for f in os.listdir("images") if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not files:
        print("(No images found)")
    else:
        for f in files:
            print(f)
    print("-" * 30)

# --- Helper to check error codes ---
def run_command(command_str):
    """ Runs a command and checks its return code. """
    return_code = os.system(command_str)
    
    if return_code != 0:
        print("\n" + "=" * 40)
        print(" !!!   E R R O R   !!!")
        print("=" * 40)
        print(f"The program failed (exit code {return_code}).")
        print("This could be a bad input image, or an")
        print("invalid number for seams.")
        print("\nPress Enter to return to the menu.")
        input()
        return False
    return True

# --- Main App Logic ---

def run_standard_carver(exe_name):
    """
    Handles the menu flow for DP, Greedy, and Graph-Cut carvers.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 40)
    print(f" Selected: {exe_name}")
    print("=" * 40 + "\n")
    check_images_folder()

    # 1. Get Input Image
    while True:
        input_file = input("Enter input image name (e.g., photo or photo.jpg): ")
        if input_file:
            break
        print("ERROR: Input name cannot be empty.")

    # 2. Get Output Image
    while True:
        output_file = input("Enter output image name (e.g., result): ")
        if output_file:
            break
        print("ERROR: Output name cannot be empty.")

    # Fix extension if missing
    if '.' not in output_file:
        output_file += ".jpg"
        print(f" (No extension provided. Saving as {output_file})")

    # 3. Get Seam Count
    while True:
        seams = input("Enter number of seams to remove (default 50): ")
        if not seams:
            seams = "50"
            break
        if seams.isdigit() and int(seams) > 0:
            break
        print("ERROR: Input must be a positive number (e.g., 50).")
    
    # 4. Get Direction
    while True:
        direction_choice = input("Enter direction - (v)ertical or (h)orizontal (default v): ").lower()
        if direction_choice in ['h', 'horizontal']:
            direction = "horizontal"
            break
        elif direction_choice in ['v', 'vertical', '']:
            direction = "vertical"
            break
        print("ERROR: Invalid input. Please enter 'v' or 'h'.")

    # 5. Get Visualization
    viz_flag = ""
    viz_display = "n"
    if exe_name == "graph_cut_seam_carving.exe":
        viz_display = "n (Not Supported)"
    else:
        viz_choice = input("Show step-by-step visualization? (y/n, default n): ").lower()
        print(" (NOTE: This will pause on every seam)")
        if viz_choice in ['y', 'yes']:
            viz_flag = "--visualize"
            viz_display = "y"

    # 6. Execute
    print("\n" + "=" * 40)
    print(" Running seam carving...")
    print("=" * 40)
    print(f"  Input:     images\\{input_file}")
    print(f"  Output:    images\\{output_file}")
    print(f"  Seams:     {seams}")
    print(f"  Direction: {direction}")
    print(f"  Visualize: {viz_display}\n")
    
    # --- Build the command ---
    command = f'{exe_name} "images\\{input_file}" "images\\{output_file}" --num_seams {seams} --direction {direction} {viz_flag}'
    
    if run_command(command):
        # 7. Run Comparison
        print("\n" + "=" * 40)
        print(" SUCCESS! Output saved.")
        print(" Creating comparison image...")
        
        comp_command = f'image_comparison_viewer.exe "images\\{input_file}" "images\\{output_file}" --save "images\\comparison.jpg" --layout vertical'
        run_command(comp_command)
        
        if os.path.exists(f"images\\comparison.jpg"):
            print(" Comparison saved as: images\\comparison.jpg")
        print("=" * 40)
        
    print("\nPress Enter to return to the menu.")
    input()


def run_interactive_tool():
    """
    Handles the menu flow for the Interactive tool.
    """
    exe_name = "interactive_seam_carving.exe"
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 40)
    print("  Interactive Resizing Tool")
    print("=" * 40 + "\n")
    check_images_folder()

    while True:
        input_file = input("Enter input image name to open (e.g., photo): ")
        if input_file:
            break
    
    print("\n Launching tool...")
    print(" - Move the sliders to resize the image.")
    print(" - (This may lag as it re-calculates!)")
    print(" - Press 's' in the window to save the result.")
    print(" - Press 'q' or ESC in the window to quit.\n")
    
    command = f'{exe_name} "images\\{input_file}"'
    run_command(command)
    
    print("\nTool closed. Press Enter to return to the menu.")
    input()

def main_menu():
    """
    The main menu loop.
    """
    exe_map = {
        "1": "dynamic_programming_seam_carving.exe",
        "2": "greedy_algorithm_seam_carving.exe",
        "3": "graph_cut_seam_carving.exe",
    }
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print("         SEAM CARVING TOOL (Python)")
        print("=" * 40)
        print("\n [Standard Algorithms]")
        print(" 1. Dynamic Programming (Optimal, Recommended)")
        print(" 2. Greedy Algorithm (Fast, Low-Quality)")
        print(" 3. Graph-Cut (Bonus, Slower than DP)")
        print("\n [Bonus Tools]")
        print(" 4. Interactive Resizing Tool (DP)")
        print(" 5. Exit")
        print("-" * 40)
        
        choice = input("Enter your choice (1-5): ")
        
        if choice in exe_map:
            run_standard_carver(exe_map[choice])
        elif choice == "4":
            run_interactive_tool()
        elif choice == "5":
            print("Thank you for using Seam Carving Tool!")
            sys.exit()
        else:
            print("Invalid choice! Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    # Set CWD to the script's directory (for PyInstaller)
    try:
        if getattr(sys, 'frozen', False):
            # This is the path to the .exe file
            application_path = os.path.dirname(sys.executable)
            os.chdir(application_path)
    except Exception as e:
        print(f"Error setting CWD: {e}")
        input() # Pause
        
    main_menu()