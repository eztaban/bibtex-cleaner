import os, shutil

def clear_folder(folder: str):
    """
    Deletes the content of a folder without removing the folder itself.

    Args:
        folder (str): Path to the folder whose content needs to be deleted.

    Raises:
        ValueError: If the specified path is not a valid directory.
    """
    if not os.path.isdir(folder):
        raise ValueError(f"The specified path '{folder}' is not a valid directory.")

    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove the file or symbolic link
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove the directory and its contents
        except Exception as e:
            print(f"Failed to delete '{item_path}'. Reason: {e}")
            
            