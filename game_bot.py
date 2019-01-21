import random
import cah

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

# CAH card data created by vdel26 (https://github.com/vdel26/cah-node-api/blob/master/src/cards.js)
# Full credit for card creation & rules by Cards Against Humanity LLC


BOT_PREFIX = "!"
TOKEN = open("secret_key.txt").readline().strip("\n")
        # a file containing only the secret key of your bot

# Client = discord.Client() # creates a new Discord Client
client_bot = Bot(command_prefix=BOT_PREFIX)


@client_bot.event
async def on_ready():
    bot = client_bot.user.name
    print('"{}" is online and connected to Discord!'.format(bot))

# Starts a new game with the game-type specified as the only param
# If there is a game of that type already going, then it returns a
#   message saying that they can instead join the ongoing game
@client_bot.command(pass_context=True)
async def startAGame(context):
    # start the game, call all the helper functions you need, and them
    # print a message quickly explaining how to join and play the game
    pass

@client_bot.command(pass_context=True)
async def joinGame(context):
    # checks if there's a game currently going
    # if there is, then it calls the join_game() function associated with that game
    pass

@client_bot.command
async def seeCurrentHand():
    # this is supposed to show the white cards you currently have
    pass

@client_bot.command(pass_context=True)
async def voteOnCard(context):
    pass

@client_bot.command(pass_context=True)
async def passUpCard(context):
    pass

@client_bot.command(pass_context=True)
async def passUpCards(context):
    passUpCard(context)


@client_bot.command
async def endGame():
    """
    Ends an active game

    :precond: the user calling this function must be the one who called startAGame()
    :return:
    """
    pass

client_bot.run(TOKEN)