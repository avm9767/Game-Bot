import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

# CAH card data created by vdel26 (https://github.com/vdel26/cah-node-api/blob/master/src/cards.js)
# Full credit for card creation & rules by Cards Against Humanity LLC


BOT_PREFIX = "~"
TOKEN = open("secret_key.txt").readline().strip("\n")
        # a file containing only the secret key of your bot

# Client = discord.Client() # creates a new Discord Client
client_bot = Bot(command_prefix=BOT_PREFIX)


@client_bot.event
async def on_ready():
    bot = client_bot.user.name
    print('"{}" is online and connected to Discord!'.format(bot))


client_bot.run(TOKEN)