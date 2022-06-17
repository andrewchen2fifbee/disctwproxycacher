# TODO use env to store bot token, target server, desired role id, ...
# TODO include flask for web stuff
# TODO twitter stuff later

# Relevant:
# ----------
# discord.py sample code, documentation
# Discord API documentation

# Third-party libraries used here:
# ----------
# discord.py        Simplify interacting with Discord
# python-dotenv     Grab environment variables from .env file
# plus the dependencies of the above

import asyncio
import logging
import time

import discord

from dotenv import load_dotenv
import os

# Environment variables
load_dotenv()
BOT_TOKEN_SUPER_SECRET = os.getenv('DISCORD_BOT_TOKEN')
SERVER_ID = int(os.getenv('DISCORD_SERVER_ID'))
VERIFIED_ROLE_ID = int(os.getenv('DISCORD_VERIFIED_ROLE_ID'))

# Log to file `DCMemTracker_YEAR-MONTH-DAY_HOUR-MINUTE-SECOND.log`
# Times are UTC
start_time = time.strftime('_%Y-%m-%d_%H-%M-%S', time.gmtime())
log_filename = 'DCMemTrackerLog' + start_time + '.log'
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Enable members intent to use guild.members
intents = discord.Intents.default()
intents.members = True


def member_has_role(member, role):
    for member_role in member.roles:
        if member_role == role:
            return True
    return False


class DiscordMemberTrackingClient(discord.Client):
    server = None
    verified_role = None
    verified_members = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        # all other init stuff is lazy, when our bot is ready (logged in, etc)
        self.bg_task = self.loop.create_task(self.my_background_task())


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.server = client.get_guild(SERVER_ID)
        self.verified_role = self.server.get_role(VERIFIED_ROLE_ID)
        print('Tracking in server', self.server.name, 'id', self.server.id)
        print('Members:')
        self.verified_members = []
        for member in self.server.members:
            print('\tMember:', member.name)
            print('\t\tVerified?: ', member_has_role(member, self.verified_role))
            self.verified_members.append(member)
            # pending = true when the user clicks through a rules screen
            #           not useful for us
        print('------')


    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(986747470283407433) # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(60) # task runs every 60 seconds


    # For dev purposes before adding web app functionality
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        # Single user check
        if message.content.startswith('$verified'):
            target = message.content[10:]
            member = None
            verified = False

            if not len(target):
                await message.channel.send('Please provide USERNAME#1111 or USERID for the user to check.')
                return
            else:
                try:
                    uuid = int(target)
                    member = self.server.get_member(uuid)
                except:
                    uname = target
                    member = self.server.get_member_named(uname)

            if member:
                verified = member_has_role(member, self.verified_role)
                await message.channel.send((':white_check_mark:' if verified else ':yellow_square:') + ' ' + member.name + '#' + member.discriminator)
            else:
                await message.channel.send('Could not find member `' + target + '`')

        # Show whole list
        if message.content.startswith('$getmems'):
            members = {member.name+'#'+member.discriminator:member_has_role(member, self.verified_role) for member in self.server.members}
            print(members)
            reply = 'Members:'
            for name, verified in members.items():
                reply += '\n' + '    '
                reply += ':white_check_mark: ' if verified else ':yellow_square: '
                reply += name
            await message.channel.send(reply)

client = DiscordMemberTrackingClient(intents=intents)
client.run(BOT_TOKEN_SUPER_SECRET)
