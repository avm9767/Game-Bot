import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

# CAH card data created by vdel26 (https://github.com/vdel26/cah-node-api/blob/master/src/cards.js)
# Full credit for card creation & rules by Cards Against Humanity LLC

available_white_cards = []
used_white_cards = []
card_czar = None

# the key for this dictionary will be the number associated with the answer card(s)
# chosen by a player with the value being a list in this order:
    # list[0] == user's name
    # list[1:] == the answer cards the user "handed" to the Card Czar. This is usually
                # just one card but can be two or more as well
current_answer_cards = {}
index = 1

available_black_cards = []
used_black_cards = []
current_black_card = None

# each player's author id will be the key while their white & black cards
# will be 2 lists within a list, so:
# { user1: [ [current white cards], [black cards won] ], user2: [[],[]], ... }
connected_players = {}

"""
This function reads the file that the cards are contained in
and separates them into their respective lists
"""
def read_file(filename):
    filename = open(filename)
    for line in filename.readlines():
        line = line.strip("\n")
        if line.endswith("[") or line.endswith("]") or line == "":
            continue
        card = line.lstrip().strip(',\"')
        if line.find("_") == -1:
            available_white_cards.append(card)
        else:
            available_black_cards.append(card)

def shuffle_cards(deck):
    random.shuffle(deck)

"""
Adds a new player to a game of CAH and gives
the player a hand of white cards

When calling this function to add the user, do
whatever.join_game(message.author)
"""
def join_game(user):
    connected_players[user] = [get_new_hand(),[]]

"""
Takes all the white cards from the user's current hand
and puts them back into the deck

When calling this function to remove the user, do
whatever.leave_game(message.author)
"""
def leave_game(user):
    leaving_user = connected_players.pop(user)
    current_hand = leaving_user[0]
    for i in range(len(current_hand)):
        available_white_cards.append(current_hand[i])
    shuffle_cards(available_white_cards)

"""
Draws a new white card from the deck of available white cards
"""
def get_new_card():
    card = random.choice(available_white_cards)
    available_white_cards.remove(card)
    return card

"""
Called at the start of a new game; gives every player
a random hand of 10 white cards

@return a list of 10 cards
"""
def get_new_hand():
    new_hand = []
    for i in range(10):
        new_hand.append(get_new_card())
    return new_hand

"""
After a round of CAH where everyone (except the Card Czar)
has put down their white cards, they all get their cards
replaced (except the Card Czar)

@param num_of_cards: the number of cards to be dealt (per person)
"""
def pick_up_cards(num_of_cards):
    new_cards = []
    for i in range(num_of_cards):
        new_cards.append(get_new_card())
    return new_cards

"""
This function needs to include the function
    message.author.send(cards as strings)
Apparently this sends the user a private message, so the cards
(in string representation) can only be messaged to the user

:return the list of white cards the user currently has
"""
async def see_current_hand(context, user):
    current_cards = connected_players[user][0]
    cards_as_string = ""
    idx = 1
    for card in current_cards:
        cards_as_string += idx,":", card, "\n"
        idx += 1
    await context.message.author.send(cards_as_string)

"""
This function is called when a player has chosen their card(s) to "hand"
to the Card Czar. Adds the card(s) to the dictionary of current_answer_cards
"""
def submit_cards(card_indexes):
    pass

"""
This function is exclusively for the current Card Czar to use;
let's the Card Czar vote on which white card was the best

@precond: all white cards have a number associated with them
          from 1 to (number of players - 1 (no Czar included));
          the Card Czar selects the card's corresponding number
          to vote for their favorite card

@param num: the number of the corresponding card that the Czar
            wants to vote for
"""
def vote_card(num):
    pass

def change_czar():
    pass

"""
Gets the number of points (aka black cards) a user has won

@return the number of black cards the user has won
"""
def get_points(user):
    player = connected_players[user]
    black_cards = player[1]
    return len(black_cards)

"""
Gets the next black card in the deck of available black cards
and prints (messages) it to the channel
"""
def print_black_card(card):
    # create an embed object here with
        # title = This round's black card:
        # description = [[[ the black card ]]]
        # color = whatever color you want as a 0x[hex_c0de] value
    # and then to this embed add:
        # embed_var_name.set_author = "{} is the Card Czar!" w/ the
            # current Card Czar's name in the braces
    embed = discord.Embed(title="Current card Czar: {}".format(card_czar), description=current_black_card)
    pass

"""
Shuffles and prints all the answer cards to the channel.
After shuffling, this function will go through the list of
answer cards and assign each answer a number before printing
them into the channel
"""
def print_answer_cards(answer_cards):
    pass