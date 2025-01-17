import os

def searchdir(directory, file_extension=None):
    """
    Loops through a directory to find files.
    
    :param directory: The path to the directory to search.
    :param file_extension: Optional. File extension to filter by (e.g., '.txt').
    :return: List of found file paths.
    """
    found_files = []
    
    try:
        for root, dirs, files in os.walk(directory):  # Traverse through all subdirectories
            for file in files:
                if file_extension:
                    if file.endswith(file_extension):  # Check file extension if specified
                        found_files.append(os.path.join(root, file))
                else:
                    found_files.append(os.path.join(root, file))  # Add all files

        return found_files
    except Exception as e:
        print(f"Error: {e}")
        return []