from discord.ext import tasks

import discord

from dotenv import load_dotenv
import os

# Environment variables
load_dotenv()
BOT_TOKEN_SUPER_SECRET = os.getenv('DISCORD_BOT_TOKEN')

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    @tasks.loop(seconds=60) # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(986747470283407433) # channel ID goes here
        self.counter += 1
        await channel.send(self.counter)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

client = MyClient()
client.run(BOT_TOKEN_SUPER_SECRET)
