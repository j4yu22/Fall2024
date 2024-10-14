"""
Course: CSE 251 
Lesson: L04 Prove
File:   prove.py
Author: Jay Underwood

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- Complete the assignments TODO sections and DO NOT edit parts you were told to leave alone.
- Review the full instructions in Canvas; there are a lot of DO NOTS in this lesson.
"""

import time
import threading
import random
from datetime import datetime

# Include cse 251 common Python files
from cse251 import *

# Global Constants - DO NOT CHANGE
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        print(f'Created: {self.info()}')
           
    def info(self):
        """ Helper function to quickly get the car information. """
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.__items = []

    def size(self):
        return len(self.__items)

    def put(self, item):
        assert len(self.__items) <= 10
        self.__items.append(item)

    def get(self):
        return self.__items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_queue, queue_full, queue_empty, queue_stats):
        threading.Thread.__init__(self)
        self.car_queue = car_queue
        self.queue_full = queue_full
        self.queue_empty = queue_empty
        self.queue_stats = queue_stats

    def run(self):
        for i in range(CARS_TO_PRODUCE):
            car = Car()

            # Wait if the queue is full
            self.queue_full.acquire()

            # Add the car to the queue
            self.car_queue.put(car)
            self.queue_stats[self.car_queue.size()] += 1

            # Signal that the queue is not empty
            self.queue_empty.release()

        # Signal that there are no more cars to be produced
        for _ in range(MAX_QUEUE_SIZE):
            self.queue_empty.release()


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, car_queue, queue_full, queue_empty):
        threading.Thread.__init__(self)
        self.car_queue = car_queue
        self.queue_full = queue_full
        self.queue_empty = queue_empty

    def run(self):
        while True:
            # Wait until the queue is not empty
            self.queue_empty.acquire()

            if self.car_queue.size() == 0:
                return

            # Get the car from the queue
            car = self.car_queue.get()
            print(f'Sold: {car.info()}')

            # Signal that there is space in the queue
            self.queue_full.release()

            # Sleep a little after selling a car
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def main():
    log = Log(show_terminal=True)

    # Create semaphores
    queue_full = threading.Semaphore(MAX_QUEUE_SIZE)  # Limits the factory when queue is full
    queue_empty = threading.Semaphore(0)  # Limits the dealership when queue is empty

    # Create queue251 
    car_queue = Queue251()

    # This tracks the length of the car queue during receiving cars by the dealership
    queue_stats = [0] * (MAX_QUEUE_SIZE + 1)

    # Create your one factory
    factory = Factory(car_queue, queue_full, queue_empty, queue_stats)

    # Create your one dealership
    dealership = Dealer(car_queue, queue_full, queue_empty)

    log.start_timer()

    # Start factory and dealership
    factory.start()
    dealership.start()

    # Wait for factory and dealership to complete
    factory.join()
    dealership.join()

    log.stop_timer(f'All {sum(queue_stats)} cars have been created and sold.')

    # Plot the statistics
    xaxis = [i for i in range(0, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count', filename='Production count vs queue size.png')


if __name__ == '__main__':
    main()
