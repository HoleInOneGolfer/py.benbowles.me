""" WSGI entry point for the Flask application. """

import sys
import os
from flask import Flask, app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

import quiz_server

BASE_PATH = os.getcwd() if os.name == "nt" else "/home/benbow/src"
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

APPS = {}

# Register the quiz_server application
qs = quiz_server.create_app()
APPS[f'/{qs.name}'] = qs

MAIN_APP = Flask(__name__, instance_relative_config=True)

@MAIN_APP.route("/")
def index():
    content = f"<h1>{MAIN_APP.name}</h1><br>"
    for path, app in APPS.items():
        content += f'<a href="{path}">{app.name}</a><br>'
    return content

application = DispatcherMiddleware(MAIN_APP, APPS)

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("localhost", 5000, application, use_debugger=True, use_reloader=True)
