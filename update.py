import subprocess
import os

# Define the path to the repository
if os.name == "nt":  # Windows
    REPO_PATH = os.getcwd()
else:
    REPO_PATH = os.path.expanduser("~/src")  # 'src' is the repository itself


def update_repo():
    try:
        # Navigate to the repository
        os.chdir(REPO_PATH)

        # Discard any uncommitted changes
        subprocess.run(["git", "reset", "--hard"], check=True)

        # Remove all untracked files and directories
        subprocess.run(["git", "clean", "-fd"], check=True)

        # Pull the latest changes from the repository
        subprocess.run(
            ["git", "pull", "origin", "main"], check=True
        )  # Replace 'main' with the correct branch name

        # Update submodules
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"], check=True
        )

        # Prune stale remote-tracking branches
        subprocess.run(["git", "remote", "prune", "origin"], check=True)

        print("Repository updated and cleaned successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    update_repo()
