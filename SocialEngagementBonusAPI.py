# Description:
# ----------
# Flask web API behavior.
# May want to save cached info to file if restarts become an issue?

# Relevant:
# ----------
# Flask documentation

# Third-party libraries used here:
# ----------
# python-dotenv     Grab environment variables from .env file
# Flask             Build/run web app (API for cached info)
# plus the many dependencies of the above

from flask import request, jsonify

from dotenv import load_dotenv
import os

load_dotenv()
KEY_TEST0 = os.getenv('OUR_API_KEY_TEST0')
ALLOWED_KEYS = [KEY_TEST0]


#...
# A general purpose error to return when we want to say something is wrong
class GenericError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    # required to be able to return this, since we need something jsonifiable
    def to_dict(self):
        if self.payload is None:
            self.payload = ()
        errDict = dict(self.payload)
        errDict['message'] = self.message
        return errDict


# Error handler so the user actually finds out why their call didn't work
# Just pass an error to them in a JSON format
def handle_generic_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def authenticate_key():
    key = request.headers.get('key', type=str)
    if key not in ALLOWED_KEYS:
        raise GenericError('Unauthorized user, key invalid', status_code=401)


def check_discord_verification(bot_client):
    username = request.args.get('username', type=str)
    if username:
        return str(bot_client.is_user_verified(username))
    else:
        raise GenericError('Please provide a username to check bonus eligibility for...', status_code=400)
