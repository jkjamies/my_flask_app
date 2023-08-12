#!/usr/bin/env python3

"""A simple Flask app."""

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def main():
    """Return the main page."""
    return '''
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''


@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    """Echo the user input."""
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text
