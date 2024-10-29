"""
Course: CSE 251 
Lesson: L06 Prove
File:   prove.py
Author: Jay Underwood

Purpose: Processing Plant

Instructions:

- Implement the necessary classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime
import json

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.json'
BOXES_FILENAME = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ Bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """
    Gift of a large marble and a bag of marbles - Don't change

    Parameters:
        large_marble (string): The name of the large marble for this gift.
        marbles (Bag): A completed bag of small marbles for this gift.
    """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver',
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda',
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green',
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange',
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink',
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple',
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango',
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink',
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green',
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple',
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue',
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue',
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow',
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink',
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink',
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue',
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, settings, pipe):
        mp.Process.__init__(self)
        self.marble_count = settings[MARBLE_COUNT]
        self.creator_delay = settings[CREATOR_DELAY]
        self.pipe = pipe

    def run(self):
        for _ in range(self.marble_count):
            marble = random.choice(self.colors)
            self.pipe.send(marble)
            time.sleep(self.creator_delay)

        self.pipe.send(None)  # Signal the end


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then sends bags to the assembler """

    def __init__(self, settings, in_pipe, out_pipe):
        mp.Process.__init__(self)
        self.bag_count = settings[NUMBER_OF_MARBLES_IN_A_BAG]
        self.bagger_delay = settings[BAGGER_DELAY]
        self.in_pipe = in_pipe
        self.out_pipe = out_pipe

    def run(self):
        bag = Bag()
        while True:
            marble = self.in_pipe.recv()
            if marble is None:
                if bag.get_size() > 0:
                    self.out_pipe.send(bag)  # Send the last incomplete bag
                self.out_pipe.send(None)  # Signal the end
                break

            bag.add(marble)
            if bag.get_size() == self.bag_count:
                self.out_pipe.send(bag)
                bag = Bag()
                time.sleep(self.bagger_delay)


class Assembler(mp.Process):
    """ Takes bags and creates gifts, then sends gifts to the wrapper """

    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, settings, in_pipe, out_pipe):
        mp.Process.__init__(self)
        self.assembler_delay = settings[ASSEMBLER_DELAY]
        self.in_pipe = in_pipe
        self.out_pipe = out_pipe

    def run(self):
        while True:
            bag = self.in_pipe.recv()
            if bag is None:
                self.out_pipe.send(None)  # Signal the end
                break

            large_marble = random.choice(self.marble_names)
            gift = Gift(large_marble, bag)
            self.out_pipe.send(gift)
            time.sleep(self.assembler_delay)


class Wrapper(mp.Process):
    """ Takes gifts and wraps them by saving to a file """

    def __init__(self, settings, in_pipe, gift_counter):
        mp.Process.__init__(self)
        self.wrapper_delay = settings[WRAPPER_DELAY]
        self.in_pipe = in_pipe
        self.gift_counter = gift_counter

    def run(self):
        with open(BOXES_FILENAME, 'w') as file:
            while True:
                gift = self.in_pipe.recv()
                if gift is None:
                    break

                timestamp = datetime.datetime.now().time()
                file.write(f'Created - {timestamp}: {gift}\n')
                with self.gift_counter.get_lock():
                    self.gift_counter.value += 1
                time.sleep(self.wrapper_delay)


def main():
    """ Main function """

    log = Log(show_terminal=True)
    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}')
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # Create Pipes
    creator_to_bagger, bagger_to_creator = mp.Pipe()
    bagger_to_assembler, assembler_to_bagger = mp.Pipe()
    assembler_to_wrapper, wrapper_to_assembler = mp.Pipe()

    # Create shared variable to count the number of gifts created
    gift_counter = mp.Value('i', 0)

    # Delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # Create the processes
    creator = Marble_Creator(settings, creator_to_bagger)
    bagger = Bagger(settings, bagger_to_creator, bagger_to_assembler)
    assembler = Assembler(settings, assembler_to_bagger, assembler_to_wrapper)
    wrapper = Wrapper(settings, wrapper_to_assembler, gift_counter)

    log.write('Starting the processes')

    # Start processes
    creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    log.write('Waiting for processes to finish')

    # Wait for processes to complete
    creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()

    display_final_boxes(BOXES_FILENAME, log)

    # Log the number of gifts created
    log.write(f'Total gifts created: {gift_counter.value}')
    log.stop_timer(f'Total time')


if __name__ == '__main__':
    main()
