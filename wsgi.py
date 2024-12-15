import sys
import os
from pathlib import Path
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from importlib import import_module

# Determine the base path for the project
# Adjust based on environment
if os.name == "nt":  # Windows
    base_path = os.getcwd()
else:  # PythonAnywhere or other *nix systems
    base_path = "/home/benbow/src"

# Add your project directory to the sys.path
if base_path not in sys.path:
    sys.path.append(base_path)


# Function to dynamically discover and import Flask apps
def discover_apps(base_path, exclude=["main"]):
    apps = {}
    base_path = Path(base_path)

    # Iterate over directories in the base path
    for app_dir in base_path.iterdir():
        if app_dir.is_dir() and app_dir.name not in exclude:
            try:
                # Import the app object from each app's __init__.py
                module = import_module(f"{app_dir.name}")
                app = getattr(module, "app", None)
                if app:
                    apps[f"/{app_dir.name}"] = app
            except Exception as e:
                print(f"Error loading app from {app_dir.name}: {e}")

    return apps


# create basic links to the other apps
def create_links(apps):
    links = []
    for path, app in apps.items():
        links.append(f'<a href="{path}">{app.name}</a>')
    return "<br>".join(links)


# Create the main app
main_app = Flask(__name__)


@main_app.route("/")
def main_index():
    return f"Hello, World!<br>{create_links(apps)}"


# Discover other apps dynamically
apps = discover_apps(base_path)

# Combine applications
application = DispatcherMiddleware(main_app, apps)
