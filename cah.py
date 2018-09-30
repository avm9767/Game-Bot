import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

# CAH card data created by vdel26 (https://github.com/vdel26/cah-node-api/blob/master/src/cards.js)
# Full credit for card creation & rules by Cards Against Humanity LLC

available_white_cards = []
used_white_cards = []
current_answer_cards = []

available_black_cards = []
used_black_cards = []

connected_players = []


# This function reads the file that the cards are contained in
# and separates them into their respective lists
def read_file(filename):
    pass

def shuffle_cards(deck):
    pass

def join_game(user):
    pass

def leave_game(user):
    pass

# Called at the start of a new game; gives every player
# a random hand of 10 white cards
def get_new_hand():
    pass

def see_current_hand(user):
    pass

# After a round of CAH where everyone (except the Card Czar)
# has put down their white cards, they all get their cards
# replaced (except the Card Czar)
#
# @param num_of_cards: the number of cards to be dealt (per person)
def pick_up_cards(num_of_cards):
    pass

# This function is exclusively for the current Card Czar to use;
# let's the Card Czar vote on which white card was the best
#
# @precond: all white cards have a number associated with them
#           from 1 to (number of players - 1 (no Czar included));
#           the Card Czar selects the card's corresponding number
#           to vote for their favorite card
#
# @param num: the number of the corresponding card that the Czar
#             wants to vote for
def vote_card(num):
    pass

# Awards a point to the user who won the vote and got the black card
def award_point(user):
    pass

def print_black_card(card):
    pass

# Function that will shuffle and print all the answer cards to the
# channel. After shuffling, this function will go through the list
# of answer cards and assign each answer a number before printing
# them into the channel
def print_answer_cards(answer_cards):
    pass