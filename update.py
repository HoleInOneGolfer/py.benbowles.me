"""
Update a Git repository and its submodules.
"""

import os
import sys

# Define the path to the repository
REPO_PATH = os.getcwd() if os.name == "nt" else os.path.expanduser("~/src")
DEFAULT_BRANCH = "main"

def update_repo(repo_path=REPO_PATH, branch=DEFAULT_BRANCH):
    """
    COMMANDS
    * `git pull origin <branch>`: Pulls the latest changes from the specified branch of the remote repository.
    * `git submodule update --init --recursive --remote`: Updates all submodules to their latest commits, initializing them if they are not already initialized.
    * `git commit -a -m "Updated submodules to latest versions"`: Commits any changes made to the submodules with a message.
    * `git push origin <branch>`: Pushes the committed changes to the specified branch of the remote repository.
    """
    print(f"Repo path: {repo_path}, Branch: {branch}", file=sys.stderr)
    # check if actually a github repository
    if not os.path.isdir(repo_path) or not os.path.exists(os.path.join(repo_path, ".git")):
        raise ValueError(f"Invalid repository: {repo_path}")

    # Change to the repository directory
    os.chdir(repo_path)
    print(f"Changed directory to: {repo_path}", file=sys.stderr)

    os.system(f"git pull origin {branch}")
    os.system("git submodule update --init --recursive --remote")
    os.system('git commit -a -m "Updated submodules to latest versions"')
    os.system(f"git push origin {branch}")

if __name__ == "__main__":
    update_repo()
