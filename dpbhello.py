import discord

from dotenv import load_dotenv
import os

# Environment variables
load_dotenv()
BOT_TOKEN_SUPER_SECRET = os.getenv('DISCORD_BOT_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$getmems'):
        return

client.run(BOT_TOKEN_SUPER_SECRET)
