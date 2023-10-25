import os
from datetime import datetime

# Folder path containing the images
folder_path = "C:\\Users\\Downloads\\images"
new_folder_path = os.path.join(os.path.dirname(folder_path), "renamed_images")

# Create the new folder if it doesn't exist
if not os.path.exists(new_folder_path):
    os.mkdir(new_folder_path)
    
# Get a list of all .jpg files in the folder
files = os.listdir(folder_path)
jpeg_files = [f for f in files if f.endswith(".jpeg")]

# Rename each file based on its creation time
for i, filename in enumerate(jpeg_files):
    # Generate a new name for the file based on the creation time
    new_name = f"full_img_{i}.jpeg"
    new_path = os.path.join(new_folder_path, new_name)

    # Rename the file and save it in the new folder
    os.rename(os.path.join(folder_path, filename), new_path)
