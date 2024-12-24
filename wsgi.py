""" WSGI entry point for the Flask application. """

import sys
import os
from pathlib import Path
from importlib import import_module
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Determine the base path for the project
BASE_PATH = os.getcwd() if os.name == "nt" else "/home/benbow/src"

# Add the base path to `sys.path` if not already present
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)


def discover_apps(base_path, exclude=None):
    """
    Dynamically discover and import Flask apps within the base path.

    Args:
        base_path (str): The directory containing potential Flask apps.
        exclude (list): Directories to exclude during discovery.

    Returns:
        dict: A mapping of URL prefixes to Flask app instances.
    """
    if exclude is None:
        exclude = [".git", "__pycache__"]

    apps = {}
    base_path = Path(base_path)

    print(f"Base path: {base_path}", file=sys.stderr)

    for app_dir in base_path.iterdir():
        if app_dir.is_dir() and app_dir.name not in exclude:
            print(f"Checking directory: {app_dir}", file=sys.stderr)
            try:
                # Import the app module dynamically
                module = import_module(app_dir.name)
                app = getattr(module, "app", None)
                if app and isinstance(app, Flask):
                    apps[f"/{app_dir.name}"] = app
                else:
                    print(
                        f"No valid Flask 'app' found in {app_dir.name}", file=sys.stderr
                    )
            except (ImportError, AttributeError) as e:
                print(
                    f"Error loading app from {app_dir.name}: {type(e).__name__} - {e}",
                    file=sys.stderr,
                )
    return apps


def create_links(apps):
    """
    Generate HTML links to all discovered apps.

    Args:
        apps (dict): A mapping of URL prefixes to Flask app instances.

    Returns:
        str: HTML containing links to the apps.
    """
    return "<br>".join(f'<a href="{path}">{app.name}</a>' for path, app in apps.items())


def create_index(apps):
    """
    Generate an index page displaying links to all apps.

    Args:
        apps (dict): A mapping of URL prefixes to Flask app instances.

    Returns:
        str: HTML for the index page.
    """
    links = create_links(apps)
    return f"<h1>{MAIN_APP.name}</h1><br>{links}"


# Initialize the main application
MAIN_APP = Flask(__name__)


@MAIN_APP.route("/")
def index():
    """Root endpoint displaying app links."""
    return create_index(APPS)


# Discover and map other applications
APPS = discover_apps(BASE_PATH)

# Combine the main app and discovered apps using DispatcherMiddleware
APPLICATION = DispatcherMiddleware(MAIN_APP, APPS)

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("localhost", 5000, APPLICATION)
