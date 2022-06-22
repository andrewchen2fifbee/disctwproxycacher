# Regularly scrape Twitter's API for recent new followers

# Third-party libraries used here:
# ----------
# requests          To make HTTP requests
# requests-oauthlib To get the latest bearer token for our app to access the API
#                   (includes oauthlib as dependency)
# python-dotenv     Grab environment variables from .env file
# plus the dependencies of the above

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import asyncio
import time

from dotenv import load_dotenv
import os

load_dotenv()
TWITTER_ACCOUNT_ID = os.getenv('TWITTER_ACCOUNT_ID')
# Defines the rate limit Twitter gives us (requests per time period)
# Time period is in minutes
REQUEST_PER_TIME = 15
TIME_PERIOD = 15
# How far apart should our requests to Twitter be, in seconds?
#   Leave time for one extra request per time period
#   Then add one second to the wait
# Currently 65 seconds
MIN_REQUEST_SPACING = ((REQUEST_PER_TIME + 1) * 60 / TIME_PERIOD) + 1
# Twitter API authentication stuff, use to fetch our token
TWITTER_APP_ID = os.getenv('TWITTER_APP_ID')
TWITTER_APP_SECRET = os.getenv('TWITTER_APP_SECRET')

# https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow
# https://api.twitter.com/oauth2/token?grant_type=client_credentials
tw_client = BackendApplicationClient(client_id=TWITTER_APP_ID)
twitter = OAuth2Session(client=tw_client)
twitter.fetch_token(token_url='https://api.twitter.com/oauth2/token',
        client_id=TWITTER_APP_ID, client_secret=TWITTER_APP_SECRET)

recent_followers = []
url = 'https://api.twitter.com/2/users/{id}/followers'.format(id=TWITTER_ACCOUNT_ID)
params = {
    'max_results': '1000'
}


async def scrape_twitter_followers():
    while True:
        dynamic_request_spacing = 0
        try:
            # Request from Twitter API: followers of target acccount
            result = twitter.get(url, params=params, timeout=30)
            json = result.json()
            response = []

            # Store result
            # TODO requests.raise_for_error()?
            if result.status_code == 200:
                recent_followers.clear()
                for user in json['data']:
                    username = user['username']
                    recent_followers.append(username.lower())
            elif result.status_code == 429:
                print('TWITTER: Scraper reached a rate limit, error code', r.status_code)
            else:
                # https://developer.twitter.com/en/support/twitter-api/error-troubleshooting
                print('TWITTER: Encountered an error, error code', r.status_code)

            # Wait + repeat. Try to wait longer if we're short on requests
            try:
                rate_limit_remaining = int(result.headers['x-rate-limit-remaining'])
                rate_limit_reset = int(result.headers['x-rate-limit-reset'])
                current_time = time.time()
                dynamic_request_spacing = (rate_limit_reset - current_time) / (rate_limit_remaining + 1)
                # print('TWITTER: Calculated dynamic request spacing of', dynamic_request_spacing,
                #         'from', rate_limit_remaining, 'more requests',
                #         'over the next', rate_limit_reset-current_time, 'seconds')
            except:
                print('TWITTER: Could not calculate dynamic request spacing. Continuing...')
        except:
            # TODO more descriptive (take the exception and show info...)
            print('TWITTER: Request failed (timeout/connection error/etc). Continuing...')

        sleep_time = max(MIN_REQUEST_SPACING, dynamic_request_spacing)
        print('TWITTER: Sleeping for', sleep_time, 'seconds...')
        await asyncio.sleep(sleep_time)


def is_user_verified(username):
    try:
        return username.lower() in recent_followers
    except:
        # TODO could improve the error response here
        print('TWITTER: Received non-string username for verification check')
        return False
