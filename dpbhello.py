import discord

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

client.run('OTg2NzQ2MTUyODIzMTkzNjgw.GIbDR0.KjJ8YFLH1AIlvAHq2DAevIt-BnlsWdFNNVkY_I')
