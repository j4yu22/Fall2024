"""
Course: CSE 251 
Lesson: L02 Team Activity
File:   team.py
Author: Jay Underwood
Purpose: Make threaded API calls with the Playing Card API http://deckofcardsapi.com

Instructions:

- Review instructions in Canvas.
"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    pass

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52
        self.deck = None

    def reshuffle(self):
        url = f'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/'


    def draw_card(self):
        url = f'https://deckofcardsapi.com/api/deck/{self.id}/draw/?count=2'

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


def options():
    print('1. Draw a card.')
    print('2. Reshuffle.')
    while True:
        option = input('Select an option: ')
        if option == '1' or option == '2':
            return option
        print('Invalid option. Try again.')

def main():
    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = "34hd9ikfkho8"

    # # Testing Code >>>>>
    # deck = Deck(deck_id)
    # for i in range(55):
    #     card = deck.draw_endless()
    #     print(f'card {i + 1}: {card}', flush=True)
    # print()
    # # <<<<<<<<<<<<<<<<<<
    choice = options()
    if choice == 1:
        card = Deck.draw_card()
        print(card)
    
    elif choice == 2:
        Deck.reshuffle()
        print('Deck is reshuffled.')
        

if __name__ == '__main__':
    main()