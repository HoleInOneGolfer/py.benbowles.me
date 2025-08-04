"""
Update a Git repository and its submodules.
"""

import subprocess
import os
import sys

# Define the path to the repository
REPO_PATH = os.getcwd() if os.name == "nt" else os.path.expanduser("~/src")

# Default branch name; replace 'main' if needed
DEFAULT_BRANCH = "main"


def run_command(command, cwd=None):
    """
    Run a shell command and handle errors gracefully.

    Args:
        command (list): The command to execute as a list.
        cwd (str): The working directory for the command (optional).

    Raises:
        RuntimeError: If the command fails.
    """
    try:
        print(f"Running command: {' '.join(command)}", file=sys.stderr)
        subprocess.run(command, cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {' '.join(command)}\nError: {e}") from e


def update_repo(repo_path, branch=DEFAULT_BRANCH):
    """
    Update the Git repository and its submodules.

    Args:
        repo_path (str): Path to the Git repository.
        branch (str): Branch name to pull from.

    Raises:
        RuntimeError: If any git command fails.
    """
    if not os.path.isdir(repo_path):
        raise ValueError(f"Invalid repository path: {repo_path}")

    print(f"Updating repository at: {repo_path}", file=sys.stderr)

    try:
        # Navigate to the repository
        os.chdir(repo_path)

        # Discard uncommitted changes
        run_command(["git", "reset", "--hard"])

        # Remove untracked files and directories
        run_command(["git", "clean", "-fd"])

        # Pull the latest changes
        run_command(["git", "pull", "origin", branch])

        # Update submodules
        run_command(["git", "submodule", "update", "--init", "--recursive", "--remote", "--merge"])

        # Prune stale remote-tracking branches
        run_command(["git", "remote", "prune", "origin"])

        print("Repository updated and cleaned successfully!")
    except RuntimeError as e:
        print(f"Error updating repository: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        update_repo(REPO_PATH)
    except (RuntimeError, ValueError) as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
