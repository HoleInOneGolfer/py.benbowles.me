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

print(f"Base path: {BASE_PATH}", file=sys.stderr)

EXCLUDE_PATHS = [".git", "__pycache__", ".github", "tests", "venv"]
APPS = {}
BASE_PATH = Path(BASE_PATH)

for PROJECT_PATH in BASE_PATH.iterdir():
    if PROJECT_PATH.is_dir() and PROJECT_PATH.name not in EXCLUDE_PATHS:
        print(f"Checking project directory: {PROJECT_PATH.name}", file=sys.stderr)
        for APP_PATH in PROJECT_PATH.iterdir():
            if APP_PATH.is_dir() and APP_PATH.name not in EXCLUDE_PATHS:
                print(f"Checking directory: {APP_PATH.name}", file=sys.stderr)
                try:
                    MODULE = import_module(f"{PROJECT_PATH.name}.{APP_PATH.name}")
                    APP_FACTORY = getattr(MODULE, "create_app", None)
                    if APP_FACTORY:
                        APP = APP_FACTORY()
                        if isinstance(APP, Flask):
                            APPS[f"/{APP_PATH.name}"] = APP
                            print(f"Discovered app: {APP.name}", file=sys.stderr)
                except ImportError as e:
                    continue


# Initialize the main application
MAIN_APP = Flask(__name__, instance_relative_config=True)


@MAIN_APP.route("/")
def index():
    CONTENT = f"<h1>{MAIN_APP.name}</h1><br>"
    CONTENT = CONTENT + "<br>".join(
        f'<a href="{path}">{app.name}</a>' for path, app in APPS.items()
    )
    return CONTENT


# Combine the main app and discovered apps using DispatcherMiddleware
APPLICATION = DispatcherMiddleware(MAIN_APP, APPS)

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("localhost", 5000, APPLICATION)
