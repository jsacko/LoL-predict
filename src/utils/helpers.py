# Fonctions utilitaires
from pathlib import Path
import yaml

def get_project_root():
    """
    Gets the project root directory, assuming this function is called
    from a file within the project, and that there's a 'pyproject.toml'
    file at the project root.
    """
    # Start from THIS file's directory
    current_file = Path(__file__).resolve() # Using resolve to get an absolute path.
    # Go up directories until we find 'pyproject.toml'
    for parent in current_file.parents: # Iterate over every parent.
        if (parent / "requirements.txt").exists(): # Checks if file exists
            return parent
    raise FileNotFoundError("Project root (with requirements.txt) not found.")

project_root = get_project_root()

def load_config(path=f"{project_root}/configs/config.yaml") -> dict:
    with open(path,"r") as f:
        config = yaml.safe_load(f)
    return config
