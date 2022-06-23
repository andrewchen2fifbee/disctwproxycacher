# QUICKSTART - TESTING
- Python 3.7+ should meet package requirements (Python 3.9+ on Windows; 3.8 has an `asyncio` bug)
- Terminal: `pip install discord.py python-dotenv flask requests requests-oauthlib` (optional, if you do python stuff: https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments)
- Go save `TEMPLATE.env` as `.env` and fill out the environment variables
- Terminal: `flask run` in the directory containing app.py to host local dev server
- Official deployment stuff: https://flask.palletsprojects.com/en/2.1.x/deploying/

# QUICKSTART - DEPLOYMENT
- TODO may need to elaborate on stuff
- Choose a WSGI server and `pip install YOUR-CHOSEN-SERVER`
- Go follow the other instructions for it
- NOTE: You need a reverse proxy if you want to host on ports 80, 443.
- Consider the following:
- `Gunicorn`: https://flask.palletsprojects.com/en/2.1.x/deploying/gunicorn/
- `Waitress`: https://flask.palletsprojects.com/en/2.1.x/deploying/waitress/
- `mod_wsgi`: https://flask.palletsprojects.com/en/2.1.x/deploying/mod_wsgi/ if you really like Apache and want to use it for the HTTP server

# NOTES
- Discord bot + Twitter scraper are run as coroutines in a separate thread. Uses `asyncio`, `threading`
- Should be able to check status of any Discord server member. However, only 1000 most recent Twitter followers will get verified for now...
- Flask app (API provider) is run synchronously in the main thread
- The verification functions are synchronous stuff called by the main thread
- Pretty sure `threading` runs all threads on a single core. OK because I/O bound, not CPU bound
- Discord bot needs to cache server members on startup. With very large servers this may add some startup delay before it's ready. Not sure how exactly it works.

# ISSUES
- Twitter scraper may start blocking the Discord bot from doing stuff if requests take long enough. `requests` library doesn't seem to support asynchronous requests. If this becomes a major issue consider asynchronous HTTP requests (`aiohttp`, `requests-futures`, `grequests`, etc)
- Twitter scraper doesn't store previous followers. It only keeps the 1000 most recent followers in memory. Expect issues related to high follower count.
