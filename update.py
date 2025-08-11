"""
Update a Git repository and install/upgrade Python packages.
The packages are specified in a requirements.txt file.
"""

import os

REPO_PATH = os.getcwd() if os.name == "nt" else os.path.expanduser("~/src")
REQUIREMENTS_FILE = os.path.join(REPO_PATH, "requirements.txt")

os.chdir(REPO_PATH)
os.system(f"git fetch origin main")
os.system(f"git reset --hard origin/main")
os.system(f"pip install --upgrade -r {REQUIREMENTS_FILE}")
