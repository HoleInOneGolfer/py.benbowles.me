""" WSGI entry point for the Flask application. """

import sys
import os
from pathlib import Path
from importlib import import_module
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Determine the base path for the project
base_path = os.getcwd() if os.name == "nt" else "/home/benbow/src"

# Add the base path to `sys.path` if not already present
if base_path not in sys.path:
    sys.path.append(base_path)


def discover_apps(_base_path, _exclude=None):
    """
    Dynamically discover and import Flask apps within the base path.

    Args:
        _base_path (str): The directory containing potential Flask apps.
        _exclude (list): Directories to exclude during discovery.

    Returns:
        dict: A mapping of URL prefixes to Flask app instances.
    """
    if _exclude is None:
        _exclude = [".git", "__pycache__", ".github"]

    _apps = {}
    _base_path = Path(_base_path)

    print(f"Base path: {_base_path}", file=sys.stderr)

    for app_dir in _base_path.iterdir():
        if app_dir.is_dir() and app_dir.name not in _exclude:
            print(f"Checking directory: {app_dir}", file=sys.stderr)
            try:
                # Import the app module dynamically
                module = import_module(app_dir.name)
                app = getattr(module, "app", None)
                if app and isinstance(app, Flask):
                    _apps[f"/{app_dir.name}"] = app
                else:
                    print(
                        f"No valid Flask 'app' found in {app_dir.name}", file=sys.stderr
                    )
            except (ImportError, AttributeError) as e:
                print(
                    f"Error loading app from {app_dir.name}: {type(e).__name__} - {e}",
                    file=sys.stderr,
                )
    return _apps


def create_links(_apps):
    """
    Generate HTML links to all discovered apps.

    Args:
        _apps (dict): A mapping of URL prefixes to Flask app instances.

    Returns:
        str: HTML containing links to the apps.
    """
    return "<br>".join(
        f'<a href="{path}">{app.name}</a>' for path, app in _apps.items()
    )


def create_index(_apps):
    """
    Generate an index page displaying links to all apps.

    Args:
        _apps (dict): A mapping of URL prefixes to Flask app instances.

    Returns:
        str: HTML for the index page.
    """
    links = create_links(_apps)
    return f"<h1>{main_app.name}</h1><br>{links}"


# Initialize the main application
main_app = Flask(__name__)


@main_app.route("/")
def index():
    """Root endpoint displaying app links."""
    return create_index(apps)


# Discover and map other applications
apps = discover_apps(base_path)

# Combine the main app and discovered apps using DispatcherMiddleware
application = DispatcherMiddleware(main_app, apps)

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("localhost", 5000, application)
