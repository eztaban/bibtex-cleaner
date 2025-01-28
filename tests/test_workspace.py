import sys
import os

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import os
import tempfile
from src.workspace import make_workspace  # Replace with the actual script name

def test_make_workspace(monkeypatch):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Mock the __file__ attribute to simulate script location
        script_path = os.path.join(temp_dir, "mock_script.py")
        with open(script_path, "w") as f:
            f.write("")  # Create an empty mock script

        # Patch the __file__ attribute in your script
        monkeypatch.setattr(f"src.workspace.__file__", script_path)

        # Run the function
        make_workspace()

        # Assert the directories are created in the parent directory
        parent_dir = os.path.abspath(os.path.join(temp_dir, os.pardir))
        assert os.path.isdir(os.path.join(parent_dir, "output"))
        assert os.path.isdir(os.path.join(parent_dir, "input"))
        assert os.path.isdir(os.path.join(parent_dir, "tmp"))

        # Ensure no extra directories or files were created in the parent directory
        created_dirs = set(os.listdir(parent_dir))
        expected_dirs = {"output", "input", "tmp"}
        assert expected_dirs.issubset(created_dirs)
