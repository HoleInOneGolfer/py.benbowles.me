"""
This is the main/default app for the pythonanywhere webapp. It doesn't do anything,
it just serves as a placeholder.
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def app1_index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
