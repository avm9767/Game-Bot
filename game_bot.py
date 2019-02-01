import datetime
import cah

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

# CAH card data created by vdel26 (https://github.com/vdel26/cah-node-api/blob/master/src/cards.js)
# Full credit for card creation & rules by Cards Against Humanity LLC

#TODO change all send message statements to client_bot.send_message(message.channel, message)
#TODO change the embeds to client_bot.send_message(message.channel, embed=embed_to_print)

BOT_PREFIX = "!"
TOKEN = open("secret_key.txt").readline().strip("\n")
        # a file containing only the secret key of your bot

# Client = discord.Client() # creates a new Discord Client
client_bot = Bot(command_prefix=BOT_PREFIX)

live_cah_game = False
game = None
starting_user = None

NEW_CAH_GAME = "A new CAH game has started! {} was first to join :stuck_out_tongue_winking_eye:"
START_GAME_ALERT = "The first black card will be shown in 30 seconds, make sure to join now for " \
                   "the highest chance of winning the most cards!"
ONGOING_GAME = "There is already an ongoing CAH game! To join the game, enter !joinGame"
NO_GAME_ERROR = "Oops! It doesn't seem like there's a game of CAH going on right now ¯\_(ツ)_/¯ " \
                "Enter !startAGame to get a new game going!"
JOINED_GAME = "{} has joined the game!"
ROUND_WINNER = "{} won the black card this round!"
NEXT_CARD_MSG = "The next black card is: "
USER_LEAVE_GAME = "{} is leaving this game. We'll miss you :("
ERROR_LEAVE_GAME = "Hmmm @{}, it doesn't seem like you're in this game of CAH :thinking:"
GAME_OVER_WINNER = "CAH is officially over! The winner is: {}"
GAME_OVER = "Aww, sad to see the game end so soon :disappointed:"
END_GAME_ERROR = "Whoops! You're not the person who started this game of CAH. If you want " \
                 "to leave the game, enter !leaveGame"


@client_bot.event
async def on_ready():
    bot = client_bot.user.name
    print('"{}" is online and connected to Discord!'.format(bot))

# Starts a new game with the game-type specified as the only param
# If there is a game of that type already going, then it returns a
#   message saying that they can instead join the ongoing game
@client_bot.command(pass_context=True)
async def startAGame(context):
    """
    Starts a game of CAH

    :param context: all information pertinent to the command call
    """
    # start the game, call all the helper functions you need, and them
    # print a message quickly explaining how to join and play the game
    global live_cah_game, game, starting_user
    user = context.message.author
    if live_cah_game:
        await client_bot.send_message(context.message.channel, ONGOING_GAME)
    else:
        live_cah_game = True
        game = cah
        game.init(user)
        # game.read_file("CAH_cards.txt")
        # game.join_game(user)
        starting_user = user
        print("This is the user who started a new game of CAH: " + user.name)
        await client_bot.send_message(context.message.channel, NEW_CAH_GAME.format(user.name))
        await client_bot.send_message(context.message.channel, START_GAME_ALERT)
        wait(10)
        await client_bot.send_message(context.message.channel, embed=game.print_black_card())

def wait(seconds):
    """
    Waits a specified number of seconds before resuming execution

    :param seconds: the number of seconds to wait
    """
    current_time = datetime.datetime.now()
    current_sec = current_time.second
    ending_sec = current_sec + seconds
    ending_min = current_time.minute
    while ending_sec >= 60:
        ending_sec -= 60
        ending_min += 1
    ending_time_secs = ending_min*60 + ending_sec
    current_time_sec = current_time.minute*60 + current_sec
    while current_time_sec <= ending_time_secs:
        time = datetime.datetime.now()
        current_time_sec = time.minute*60 + time.second
    print("CAH is officially starting! First card is out!")

@client_bot.command(pass_context=True)
async def joinGame(context):
    """
    If there's already an ongoing game of CAH, the user who calls this command joins the game

    :param context: all information pertinent to the command call
    :return: a message to the channel announcing that the user joined, or that the game doesn't exist
    """
    # checks if there's a game currently going
    # if there is, then it calls the join_game() function associated with that game
    global game
    if live_cah_game is False:
        await client_bot.send_message(context.message.channel, NO_GAME_ERROR)
    else:
        user = context.message.author
        game.join_game(user) # keep in mind this is passing in the *user*, not the user's NAME
        await client_bot.send_message(context.message.channel, JOINED_GAME.format(user.name))

@client_bot.command(pass_context=True)
async def leaveGame(context):
    """
    Removes a user from an ongoing game of CAH

    :param context: all information pertinent to the command call
    :return: sends a message to the channel describing whether or not the user successfully
    left (if they were removed)
    """
    global game
    user = context.message.author
    success = game.leave_game(user)
    if success:
        await client_bot.send_message(context.message.channel, USER_LEAVE_GAME.format(user.name))
    else:
        await client_bot.send_message(context.message.channel, ERROR_LEAVE_GAME.format(user.name))

@client_bot.command(pass_context=True)
async def seeCurrentHand(context):
    """
    Shows a user their current hand of white cards

    :param context: all information pertinent to the command call
    :return: a private message to the user of their current hand of white cards
    """
    global game
    cards_string = game.see_current_hand(context.message.author)
    await client_bot.send_message(context.message.author, cards_string)

@client_bot.command(pass_context=True)
async def voteOnCard(context):
    """
    Votes on the card that the Card Czar thought was best

    :param context: all information pertinent to the command call
    :return: a message announcing who the round winner was & an embed of the next
    black card
    """
    global game
    vote = context.message.content
    vote = int(vote.strip("!voteOnCard "))
    winner = game.vote_card(vote)
    await client_bot.send_message(context.message.channel, ROUND_WINNER.format(winner))
    game.change_czar()
    black_card = game.print_black_card()
    await client_bot.send_message(context.message.channel, NEXT_CARD_MSG)
    await client_bot.send_message(context.message.channel, embed=black_card)

@client_bot.command(pass_context=True)
async def passUpCard(context):
    """
    Passes up a user's card to the Card Czar so that they can be voted on

    :param context: all information pertinent to the command call
    :return: if all users have passed up their cards, an embed of all the answer cards
    is messaged to the channel
    """
    global game
    cards = context.message.content
    card_indices = cards.split(" ")
    card_indices = card_indices[1:]
    for i in range(len(card_indices)):
        card_indices[i] = int(card_indices[i])
    answer_cards = game.submit_cards(context.message.author, card_indices)
    if answer_cards is not None:
        await client_bot.send_message(context.message.channel, embed=answer_cards)

@client_bot.command(pass_context=True)
async def passUpCards(context):
    """
    Passes up a user's cards to the Card Czar (multiple cards)

    :param context: all information pertinent to the command call
    """
    passUpCard(context)

@client_bot.command(pass_context=True)
async def endGame(context):
    """
    Ends an active game

    :precond: the user calling this function must be the one who called startAGame()
    :return:
    """
    global starting_user, game, live_cah_game
    user = context.message.author
    if user is starting_user:
        winner = game.get_winner()
        if winner is not None:
            await client_bot.send_message(context.message.channel, GAME_OVER_WINNER.format(winner))
        else:
            await client_bot.send_message(context.message.channel, GAME_OVER)
        game = None
        live_cah_game = False
    else:
        await client_bot.send_message(context.message.channel, END_GAME_ERROR)

@client_bot.command(pass_context=True)
async def trampoline(context):
    user = context.message.author
    if user.name is "Bepatt":
        image_link = "http://c.shld.net/rpx/i/s/i/spin/10092133/prod_2319165012??hei=64&amp;wid=64&amp;qlt=50"
        await client_bot.send_message(context.message.channel, image_link)

client_bot.run(TOKEN)