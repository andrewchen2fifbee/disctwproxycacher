# QUICKSTART - TESTING
- Python 3.7+ should meet package requirements (Python 3.9+ on Windows; 3.8 has an `asyncio` bug)
- Terminal: `pip install discord.py python-dotenv flask requests requests-oauthlib` (optional, if you do python stuff: https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments)
- Go save `TEMPLATE.env` as `.env` and fill out the environment variables
- Terminal: `flask run` in the directory containing app.py to host local dev server
- Official deployment stuff: https://flask.palletsprojects.com/en/2.1.x/deploying/

# QUICKSTART - DEPLOYMENT
- TODO :(

# NOTES
- Discord bot + Twitter scraper are run as coroutines in a separate thread. Uses `asyncio`, `threading`
- Flask app (API provider) is run synchronously in the main thread
- The verification functions are synchronous stuff called by the main thread
- Pretty sure `threading` runs all threads on a single core. OK because I/O bound, not CPU bound

# ISSUES
- Twitter scraper may start blocking the Discord bot from doing stuff if requests take long enough. `requests` library doesn't seem to support asynchronous requests. If this becomes a major issue consider asynchronous HTTP requests (`aiohttp`, `requests-futures`, `grequests`, etc)
