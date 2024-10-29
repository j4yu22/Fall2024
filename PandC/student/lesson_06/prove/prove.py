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
from datetime import datetime
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
              'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 
              'Orange Soda', 'Maximum Purple', 'Neon Pink', 'Light Orchid', 
              'Russian Violet', 'Sheen Green', 'Isabelline', 'Ruby', 'Emerald', 
              'Middle Red Purple', 'Royal Orange', 'Dark Fuchsia', 'Slate Blue', 
              'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 'Stop Red', 
              'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 'Maximum Blue', 
              'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 'Fiery Rose', 
              'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
              'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 
              'Dark Moss Green', 'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 
              'Rose Quartz', 'Purple', 'Almond', 'Zomp', 'Middle Green Yellow', 
              'Auburn', 'Chinese Red', 'Cobalt Blue', 'Lumber', 'Honeydew', 
              'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
              'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 
              'Royal Red', 'Arylide Yellow', 'Rose Dust', 'Terra Cotta', 'Lemon Lime', 
              'Bistre Brown', 'Venetian Red', 'Brink Pink', 'Russian Green', 
              'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 'Safety Yellow', 
              'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple', 
              'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 
              'Royal Blue', 'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, settings, out_queue):
        mp.Process.__init__(self)
        self.marble_count = settings[MARBLE_COUNT]
        self.creator_delay = settings[CREATOR_DELAY]
        self.out_queue = out_queue

    def run(self):
        for _ in range(self.marble_count):
            marble = random.choice(Marble_Creator.colors)
            self.out_queue.put(marble)
            time.sleep(self.creator_delay)

        self.out_queue.put(None)  


class Bagger(mp.Process):
    def __init__(self, settings, in_queue, out_queue):
        mp.Process.__init__(self)
        self.bag_count = settings[NUMBER_OF_MARBLES_IN_A_BAG]
        self.bagger_delay = settings[BAGGER_DELAY]
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            bag = Bag()
            for _ in range(self.bag_count):
                marble = self.in_queue.get()
                if marble is None:
                    self.out_queue.put(None)  # Signal no more bags
                    return

                bag.add(marble)

            self.out_queue.put(bag)
            time.sleep(self.bagger_delay)


class Assembler(mp.Process):
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, settings, in_queue, out_queue):
        mp.Process.__init__(self)
        self.assembler_delay = settings[ASSEMBLER_DELAY]
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            bag = self.in_queue.get()
            if bag is None:
                self.out_queue.put(None)  # Signal no more gifts
                return

            large_marble = random.choice(Assembler.marble_names)
            gift = Gift(large_marble, bag)
            self.out_queue.put(gift)
            time.sleep(self.assembler_delay)


class Wrapper(mp.Process):
    def __init__(self, settings, in_queue, gift_counter):
        mp.Process.__init__(self)
        self.wrapper_delay = settings[WRAPPER_DELAY]
        self.in_queue = in_queue
        self.gift_counter = gift_counter

    def run(self):
        with open(BOXES_FILENAME, 'w') as file:
            while True:
                gift = self.in_queue.get()
                if gift is None:
                    break

                timestamp = datetime.now().time()
                file.write(f'Created - {timestamp}: {gift}\n')
                with self.gift_counter.get_lock():
                    self.gift_counter.value += 1
                time.sleep(self.wrapper_delay)


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file - Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')


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

    # Create Queues between creator -> bagger -> assembler -> wrapper
    creator_bagger_queue = mp.Queue()
    bagger_assembler_queue = mp.Queue()
    assembler_wrapper_queue = mp.Queue()

    # Create variable to be used to count the number of gifts
    gift_counter = mp.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # Create the processes
    creator = Marble_Creator(settings, creator_bagger_queue)
    bagger = Bagger(settings, creator_bagger_queue, bagger_assembler_queue)
    assembler = Assembler(settings, bagger_assembler_queue, assembler_wrapper_queue)
    wrapper = Wrapper(settings, assembler_wrapper_queue, gift_counter)

    log.write('Starting the processes')
    
    # Start the processes
    creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    log.write('Waiting for processes to finish')
    
    # Wait for processes to finish
    creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    log.write(f'Total gifts created: {gift_counter.value}')
    log.stop_timer(f'Total time')


if __name__ == '__main__':
    main()
