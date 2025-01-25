import os

def make_workspace():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the parent directory of the script's location
    parent_dir = os.path.join(script_dir, os.pardir)
    
    # Create folders in the parent directory
    os.makedirs(os.path.join(parent_dir, "output"), exist_ok=True)
    os.makedirs(os.path.join(parent_dir, "input"), exist_ok=True)
    os.makedirs(os.path.join(parent_dir, "tmp"), exist_ok=True)

make_workspace()
