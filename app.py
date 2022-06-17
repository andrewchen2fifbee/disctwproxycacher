# Used to run the Flask app and all the stuff it depends on
import SocialEngagementBonusAPI as api
from flask import Flask

import

from dotenv import load_dotenv
import os

# TODO get discord bot, twitter thing going

# TODO figure out hosting, ...
#       https://flask.palletsprojects.com/en/2.1.x/deploying/

app = Flask(__name__)


@app.errorhandler(api.GenericError)
def wrapper_error(error):
    return api.handle_generic_error(error)


@app.before_request
def wrapper_authentication():
    return api.authenticate_key()


# Only responds to GET, HEAD, OPTIONS requests by default
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
@app.route('/player-bonus-verification/discord')
def wrapper_check_discord_verification():
    return api.check_discord_verification()


# Run server
# NOTE: Debug mode gives a debugger that allows code execution.
#       Really really make sure DEBUG IS OFF for PRODUCTION SERVERS.
if __name__ == "__app__":
    app.run(host="0.0.0.0", port=80, threaded=True, debug=False)
