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
REQUEST_SPACING = ((REQUEST_PER_TIME + 1) * 60 / TIME_PERIOD) + 1
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
headers = {
    'TODO'
}

async def scrape_twitter_followers():
    while True:
        # Request from Twitter API: followers of target acccount
        json = twitter.get(url, params=params).json()
        response = []
        # TODO what if request blocked due to rate limit?
        # TODO what if request failed for other reasons?
        # Store result
        recent_followers.clear()
        for user in json['data']:
            username = user['username']
            recent_followers.append(username.lower())
        # Wait + repeat
        print('Sleeping for:', REQUEST_SPACING)
        await asyncio.sleep(REQUEST_SPACING)


def is_user_verified(username):
    try:
        return username.lower() in recent_followers
    except:
        print('TWITTER: Received non-string username for verification check')
        return False

# twitter_scraper_task = asyncio.get_event_loop().create_task(scrape_twitter_followers())
asyncio.run(scrape_twitter_followers())
