#!/usr/bin/python3
"""
Creates a Flask web server
"""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text=None):
    to_return = f"c{text.replace('_', ' ')}"
    return to_return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
