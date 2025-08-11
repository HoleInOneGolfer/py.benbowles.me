"""
Update a Git repository and install/upgrade Python packages.
The packages are specified in a requirements.txt file.
"""

import os

REPO_PATH = os.getcwd() if os.name == "nt" else os.path.expanduser("~/src")
DEFAULT_BRANCH = "main"
REQUIREMENTS_FILE = os.path.join(REPO_PATH, "requirements.txt")

def update_repository():
    """
    Update the Git repository to the latest commit on the default branch.
    """
    os.chdir(REPO_PATH)
    os.system(f"git fetch origin {DEFAULT_BRANCH}")
    os.system(f"git reset --hard origin/{DEFAULT_BRANCH}")

def install_requirements():
    """
    Install or upgrade Python packages from the requirements.txt file.
    """
    if os.path.exists(REQUIREMENTS_FILE):
        os.system(f"pip install --upgrade -r {REQUIREMENTS_FILE}")
    else:
        print(f"Requirements file not found: {REQUIREMENTS_FILE}")

def main():
    """
    Main function to update the repository and install requirements.
    """
    print("Updating repository...")
    update_repository()

    print("Installing requirements...")
    install_requirements()

    print("Update complete.")

if __name__ == "__main__":
    main()
