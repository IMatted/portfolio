"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)
"""

# Project 4 Imports
import flask
from flask import Flask, redirect, url_for, request, render_template, jsonify
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import logging

# Project 5 Imports:
from pymongo import MongoClient
import os

# WINDOWS CLIENT:
# client = MongoClient('mongodb://db:27017/')
client = MongoClient(host=os.environ.get('DB_PORT_27017_TCP_ADDR', 'db'), port=27017)
db = client.brevetsdb

# Global Variables
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY


# Pages
@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

# Project 5 Methods
@app.route("/_insert", methods=["POST"])
def insert():
    try:
        input_data = request.get_json()
        items = input_data.get("items", [])

        if not items:
            return jsonify(result="Error: No Control Times to Submit"), 400
        
        db.brevets_list.insert_one({"times": items})

        return jsonify(result="Successfully Added Entry to Database")
    except Exception as e:
        return jsonify(result=f"Server Error: {str(e)}"), 500
    
@app.route("/display")
def display():
    items = list(db.brevets_list.find())
    return render_template('display.html', items=items)


# AJAX request handlers, These return JSON, rather than rendering pages.
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 0, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    brevet_dist = request.args.get('brevet_dist', 200, type=int)
    start_time = request.args.get('start_time', type=str)

    open_time = acp_times.open_time(km, brevet_dist, start_time)
    close_time = acp_times.close_time(km, brevet_dist, start_time)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")