"""
Course: CSE 251 
Lesson: L05 Prove
File:   prove.py
Author: Jay Underwood

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier!
- Do not use try...except statements.
- You are not allowed to use the normal Python Queue object. You must use Queue251.
- The shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE.
"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Constants.
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
        self.__max_size = 0

    def get_max_size(self):
        return self.__max_size

    def put(self, item):
        self.__items.append(item)
        if len(self.__items) > self.__max_size:
            self.__max_size = len(self.__items)

    def get(self):
        return self.__items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """
    def __init__(self, queue, sem, factory_barrier, queue_condition):
        super().__init__()
        self.cars_to_produce = random.randint(200, 300) # DO NOT change
        self.queue = queue
        self.sem = sem
        self.factory_barrier = factory_barrier
        self.queue_condition = queue_condition
        self.cars_produced = 0

    def run(self):
        for _ in range(self.cars_to_produce):
            car = Car()
            self.sem.acquire()
            with self.queue_condition:
                self.queue.put(car)
                self.queue_condition.notify_all()
            self.cars_produced += 1

        self.factory_barrier.wait()

        if threading.current_thread() == threading.main_thread():
            self.sem.release()


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """
    def __init__(self, queue, sem, dealer_stats, dealer_id, queue_condition):
        super().__init__()
        self.queue = queue
        self.sem = sem
        self.dealer_stats = dealer_stats
        self.dealer_id = dealer_id
        self.queue_condition = queue_condition

    def run(self):
        while True:
            with self.queue_condition:
                while len(self.queue._Queue251__items) == 0:
                    self.queue_condition.wait()

                car = self.queue.get()
                if car is None:
                    break

                self.dealer_stats[self.dealer_id] += 1
                self.sem.release()

            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))


def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """
    sem = threading.Semaphore(MAX_QUEUE_SIZE)
    car_queue = Queue251()

    queue_lock = threading.Lock()
    queue_condition = threading.Condition(queue_lock)

    factory_barrier = threading.Barrier(factory_count)
    dealer_stats = list([0] * dealer_count)

    factories = [Factory(car_queue, sem, factory_barrier, queue_condition) for _ in range(factory_count)]

    dealers = [Dealer(car_queue, sem, dealer_stats, i, queue_condition) for i in range(dealer_count)]

    log.start_timer()

    for dealer in dealers:
        dealer.start()

    for factory in factories:
        factory.start()

    for factory in factories:
        factory.join()

    with queue_lock:
        for _ in range(dealer_count):
            car_queue.put(None)
        queue_condition.notify_all()

    for dealer in dealers:
        dealer.join()

    factory_stats = [factory.cars_produced for factory in factories]

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created.')

    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : Made = {sum(dealer_stats)} @ {factory_stats}')
        log.write(f'Dealer Stats   : Sold = {sum(factory_stats)} @ {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':
    log = Log(show_terminal=True)
    main(log)
