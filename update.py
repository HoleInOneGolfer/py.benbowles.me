import subprocess
import os

# Define the path to the repository
REPO_PATH = os.path.expanduser("~/src")  # 'src' is the repository itself


def update_repo():
    try:
        # Navigate to the repository
        os.chdir(REPO_PATH)

        # Pull the latest changes from the repository
        subprocess.run(
            ["git", "pull", "origin", "main"], check=True
        )  # Replace 'main' with the correct branch name

        # Update submodules
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"], check=True
        )

        print("Repository and submodules updated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    update_repo()
