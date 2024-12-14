import sys
from pathlib import Path
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from importlib import import_module

# Add your project directory to the sys.path
path = "/home/benbow/src"
if path not in sys.path:
    sys.path.append(path)


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


# Import the main app
from main import app as main_app

# Discover other apps dynamically
apps = discover_apps(path)

# Combine applications
application = DispatcherMiddleware(main_app, apps)
