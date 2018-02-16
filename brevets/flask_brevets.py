"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

# docker build -t brevets .
# docker run -p 5000:5000 brevets
# http://127.0.0.1:5000

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html') # renders main page


@app.errorhandler(404) # error handler
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    
    # gets all arguments needed to calculating opening and closing times
    km = request.args.get('km', 999, type=float)
    brevet_dist = request.args.get('brev_dis', 999, type=int)
    start_time = request.args.get('start_t', 999, type=str)
    start_date = request.args.get('start_d', 999, type=str)
    
    # debug statements
    app.logger.debug("start time={}".format(start_time))
    app.logger.debug("start date={}".format(start_date))
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    
    # reformats times to correct iso string format
    time_str = "{}T{}".format(start_date, start_time)
    time = arrow.get(time_str)
    time = time.isoformat() 
    
    # calculates new opening and closing times for control
    opening = acp_times.open_time(km, brevet_dist, time)
    closing = acp_times.close_time(km, brevet_dist, time)

    result = {"open": opening, "close": closing}

    return flask.jsonify(result=result) # sends back result!


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
