import random
import json
# after I get these functions coded, I want to use online JSON files to get card decks,
# mainly from https://www.crhallberg.com/cah/ but I just noticed that all JSON pages
# generated have the exact same url extension, so now idk if it'll work

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
    # list[1] == the answer cards the user "handed" to the Card Czar as a list (aka [ name, [cards] ])
                # This is usually just one card but can be two or more as well
current_answer_cards = {}
index = 1

available_black_cards = []
current_black_card = None

# each player's author id will be the key while their white & black cards
# will be 2 lists within a list, so:
# { user1 : [ [current white cards], [black cards won] ], user2 : [[],[]], ... }
connected_players = {}
all_players = []

def init(user):
    """
    Initializes a game of CAH by getting the decks of cards ready and adding the first user
    (the one who started the game)

    :param user: the user who started the game
    """
    read_file("CAH_cards.txt")
    join_game(user)

def read_file(filename):
    """
    This function reads the file that the cards are contained in and separates
    them into their respective lists

    :param filename: the name of the file containing the card decks
    """
    filename = open(filename)
    for line in filename.readlines():
        line = line.strip("\n")
        if line.endswith("[") or line.endswith("]") or line == "":
            continue
        card = line.lstrip().strip(',\"')
        if line.find("_") == -1:
            available_white_cards.append(card)
        elif line.endswith("?"):
            available_black_cards.append(card)
        else:
            available_black_cards.append(card)
    random.shuffle(available_black_cards)
    random.shuffle(available_white_cards)


def join_game(user):
    """
    Adds a new player to a game of CAH and gives the player a hand of white cards.

    When calling this function to add the user, do whatever.join_game(message.author)

    :param user: the user joining the game
    :return: a string announcing the user who has joined the game
    """
    global card_czar, current_black_card, available_black_cards
    connected_players[user] = [get_new_hand(),[]]
    all_players.append(user)
    if len(connected_players) == 1:
        card_czar = user
        all_players.remove(user)
        current_black_card = available_black_cards.pop(0)

def leave_game(user):
    """
    Takes all the white cards from the user's current hand and puts them back
    into the deck

    :param user: the user leaving
    :return: True if the user exists and was removed, else False
    """
    leaving_user = connected_players.pop(user)
    if leaving_user is None:
        return False
    all_players.remove(user)
    # gotta figure out what to do when the player who left was the Card Czar
    current_hand = leaving_user[0]
    for i in range(len(current_hand)):
        available_white_cards.append(current_hand[i])
    random.shuffle(available_white_cards)
    return True

def get_new_card():
    """
    Draws a new white card from the deck of available white cards

    :return: returns a white card from the available deck
    """
    if len(available_white_cards) == 0:
        recycle_cards()
    card = random.choice(available_white_cards)
    available_white_cards.remove(card)
    return card

def get_new_hand():
    """
    Called at the start of a new game; gives every player a random hand of
    10 white cards

    :return: a list of 10 cards
    """
    new_hand = []
    if len(available_white_cards) < 10:
        recycle_cards()
    for i in range(10):
        new_hand.append(get_new_card())
    return new_hand

def recycle_cards():
    """
    When there are not enough available white cards to hand out, the used white
    cards will be added into the deck of available white cards and then shuffled
    """
    for card in used_white_cards:
        available_white_cards.append(card)
    random.shuffle(available_white_cards)

def pick_up_cards(num_of_cards):
    """
    After a round of CAH where everyone (except the Card Czar) has put down
    their white cards, they all get their cards replaced (except the Card Czar)

    :param num_of_cards: the amount of cards to replace
    :return: new white cards from the available deck
    """
    new_cards = []
    for i in range(num_of_cards):
        new_cards.append(get_new_card())
    return new_cards

def see_current_hand(user):
    """
    This function needs to include the function message.author.send(cards as strings)

    Apparently this sends the user a private message, so the cards (in string
    representation) can only be messaged to the user

    :param user: the user requesting to see their hand of cards
    :return: the user's current hand in string representation
    """
    current_cards = connected_players[user][0]
    cards_as_string = "Here's your current hand of white cards: \n"
    idx = 1
    for card in current_cards:
        cards_as_string += str(idx) + ": " + card + "\n"
        idx += 1
    return cards_as_string

def submit_cards(user, card_indices):
    """
    This function is called when a player has chosen their card(s) to "hand"
    to the Card Czar. Adds the card(s) to the dictionary of current_answer_cards

    :param user: the user that is submitting their cards
    :param card_indices: the numbers associated with the cards being submitted
    :return: an embed of the answer cards if all players have submitted their cards, else None
    """
    global index
    answer_cards = []
    for num in card_indices:
        card = connected_players[user][0].pop(int(num)-1) # removes the card from the user's hand
        answer_cards.append(card)
    current_answer_cards[index] = [user, answer_cards]

    if index == (len(connected_players) - 1):
        index = 1
        return print_answer_cards()
    else:
        index += 1
        return None


def vote_card(num):
    """
    This function is exclusively for the current Card Czar to use;
    let's the Card Czar vote on which white card was the best

    :precond: all white cards have a number associated with them
              from 1 to (number of players - 1 (no Czar included));
              the Card Czar selects the card's corresponding number
              to vote for their favorite card
    :param num: num the number of the corresponding card that the Czar
                wants to vote for
    :return: the person associated with the winning card(s)
    """
    # get the card(s) associated with the number
    # get the user associated with the card(s)
    # add the black card to their list of won black cards
    winning_card = current_answer_cards[int(num)]
    winner = winning_card[0]
    connected_players[winner][1].append(current_black_card)
    return winner

def change_czar():
    """
    Changes who the Card Czar is when a round ends
    """
    global card_czar, available_black_cards, current_black_card
    all_players.append(card_czar)
    user = all_players.pop(0)
    all_players.remove(user)
    card_czar = user
    black_card = available_black_cards.pop(0)
    current_black_card = black_card

def get_points(user):
    """
    Gets the number of points (aka black cards) a user has won

    :param user: the user requesting to see how many points they have
    :return: the number of black cards the user has won
    """
    player = connected_players[user]
    black_cards = player[1]
    return len(black_cards)

def print_black_card(): # I used to have a card parameter here
    """
    Gets the next black card in the deck of available black cards
    and prepares an embed to be printed

    :return: the embed representing the current round's black card
    """
    # create an embed object here with
        # title = This round's black card:
        # description = [[[ the black card ]]]
        # color = whatever color you want as a 0x[hex_c0de] value
    # and then to this embed add:
        # embed_var_name.set_author = "{} is the Card Czar!" w/ the
            # current Card Czar's name in the braces

    # to post the embed, do 'await bot_client.say(embed)' or 'await bot_client.send_message(message.channel, embed=embed)'
    embed = discord.Embed(title="Current card Czar: {}".format(card_czar.name),
                          description=current_black_card,
                          color=discord.Color.blue())
    embed.set_author(name="Black card in play")
    avatar = card_czar.avatar_url
    # print(avatar)
    if avatar == "":
        avatar = card_czar.default_avatar_url
    # avatar = card_czar.default_avatar_url
    print(avatar)
    embed.set_thumbnail(url=avatar)
    return embed

# This used to have a parameter "answer_cards"; depending on how I choose to change
# implementation later, this may get changed
def print_answer_cards():
    """
    Shuffles and prints all the answer cards to the channel. After shuffling,
    this function will go through the list of answer cards and assign each
    answer a number before printing them into the channel

    :return: an embed formatted to hold all the answer cards
    """
    num = 1
    answer_cards_string = ""
    for cards in current_answer_cards.values():
        answer_cards = cards[1]
        answer_cards_string += str(num) + ": "
        for i in range(len(answer_cards)):
            card = answer_cards[i]
            answer_cards_string += card
            if i != len(answer_cards):
                answer_cards_string += ", "
        answer_cards_string += "\n"
        num += 1

    embed = discord.Embed(title="Current card Czar: {}".format(card_czar),
                          description=answer_cards_string,
                          color=discord.Color.red())
    embed.set_author(name="Answer cards submitted:")
    return embed

def get_winner():
    """
    Gets the user that has the most black cards when a game of CAH has ended

    :return: the user that had the most black cards
    """
    winner = None
    max_cards_won = 0
    for user in connected_players.keys():
        black_cards = connected_players[user][1]
        if len(black_cards) > max_cards_won:
            winner = user
            max_cards_won = len(black_cards)
    return winner
