# This script takes the file names in the current folder and makes a folder in the parent directory for each file in this folder. Yup

import os

# Get current directory
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)

# Get the name of the script so we don't create this one too as a folder
script_name = os.path.basename(__file__)

# Loop through files in the current directory
for file in os.listdir(current_dir):
    file_path = os.path.join(current_dir, file)
    # Ensure file is a file
    if os.path.isfile(file_path) and file != script_name:
        # Remove file extension
        folder = os.path.splitext(file)[0]
        # Define path for new folder
        new_dir_path = os.path.join(parent_dir, folder)
        # Check if folder already exists to prevent duplicates
        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)
            print(f"Created Folder {new_dir_path}")

print("Done! Quitting...")