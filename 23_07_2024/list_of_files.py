import os

# Specify the directory you want to scan
directory_path = '/home/ubuntu/ganecos-backend1/new_version_1_1_1/cam3_detectron2_Model/cam3_videos_json/uploaded_json'

# Get a list of all files and directories in the specified path
all_files = os.listdir(directory_path)

# Filter out only files (excluding directories)
file_names = [f for f in all_files if os.path.isfile(os.path.join(directory_path, f))]

# Print the list of file names
print(file_names)
