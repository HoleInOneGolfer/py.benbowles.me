""" This is a sample test app. """

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    """
    Root endpoint displaying app information.

    Returns:
        str: A greeting message.
    """
    return "Test App!"
