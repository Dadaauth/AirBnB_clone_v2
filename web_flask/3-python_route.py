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
    to_return = f"C {text.replace('_', ' ')}"
    return to_return


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    to_return = f"Python {text.replace('_', ' ')}"
    return to_return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
