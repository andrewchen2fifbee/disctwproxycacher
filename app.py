# Proxy caching web app to help award Discord/Twitter/other social media bonuses
# For local testing: https://github.com/discord/discord-example-app#set-up-interactivity
#                    (Use ngrok url as Roblox request destination)

# Web app behavior
import SocialEngagementBonusAPI as api
from flask import Flask

# Interact w/ Discord, Twitter, cache and check results
import DiscordBot as discord_bot
import TwitterFollowScraper as scraper

# Flask, discord.py are both blocking when run directly
# Run them on separate threads, can still share stuff
#       (share objects instead of database/files/...; API doesn't modify so it's OK)
import asyncio
from threading import Thread
from time import sleep

# These go on a separate thread
# https://discordpy.readthedocs.io/en/stable/api.html#discord.Client.start
# https://stackoverflow.com/questions/55030714/c-python-asyncio-running-discord-py-in-a-thread
event_loop = asyncio.get_event_loop()
event_loop.create_task(discord_bot.client.start(discord_bot.BOT_TOKEN_SUPER_SECRET))
event_loop.create_task(scraper.scrape_twitter_followers())

# TODO figure out hosting, ...
#       https://flask.palletsprojects.com/en/2.1.x/deploying/
# TODO Logging for Flask + Twitter stuff
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
    return api.check_discord_verification(discord_bot.client)


@app.route('/player-bonus-verification/twitter')
def wrapper_check_twitter_verification():
    return api.check_twitter_verification(scraper)


# Run server
# NOTE: Debug mode gives a debugger that allows code execution.
#       Really really make sure DEBUG IS OFF for PRODUCTION SERVERS.
print('ALL: Starting up...')
print('FLASK: Starting web app...')
if __name__ == "__app__":
    app.run(host='0.0.0.0', port=80, threaded=True, debug=False)

# Daemon threads die when all non-daemon threads (in this case, main thread) die
print('TWITTER: Starting Twitter scraper...')
print('DISCORD: Starting Discord bot...')
Thread(target=event_loop.run_forever, daemon=True).start()
