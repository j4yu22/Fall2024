"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting(id):
    print(f'Cleaner: {id} waiting...')
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting(id):
    print(f'Guest: {id} waiting...')
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))


def cleaner(room_lock, light_lock, cleaning_signal, stop_event, cleaner_id, cleaned_count):
    """
    Cleaner process: Waits for the signal to clean, cleans the room after lights are off, and increments the clean count.
    """
    while not stop_event.is_set():
        cleaner_waiting(cleaner_id)  # Simulate waiting
        cleaning_signal.acquire()  # Wait for lights to turn off

        with light_lock:  # Ensure only one cleaner enters at a time
            print(STARTING_CLEANING_MESSAGE)
            cleaner_cleaning(cleaner_id)  # Simulate cleaning
            print(STOPPING_CLEANING_MESSAGE)
            cleaned_count.value += 1


def guest(room_lock, light_lock, cleaning_signal, guest_count, party_count, stop_event, guest_id):
    """
    Guest process: Simulates entering the room, partying, and leaving.
    """
    while not stop_event.is_set():
        guest_waiting(guest_id)  # Simulate waiting
        room_lock.acquire()  # Get access to the room

        if guest_count.value == 0:
            with light_lock:  # First guest turns on the lights
                print(STARTING_PARTY_MESSAGE)
                party_count.value += 1

        guest_count.value += 1
        current_count = guest_count.value
        print(f"Guest: {guest_id}, count = {current_count}")

        room_lock.release()  # Allow others to enter

        guest_partying(guest_id, current_count)  # Simulate partying

        room_lock.acquire()  # Check if this guest is the last to leave
        guest_count.value -= 1
        if guest_count.value == 0:
            with light_lock:  # Last guest turns off the lights
                print(STOPPING_PARTY_MESSAGE)
                cleaning_signal.release()  # Notify the cleaners
        room_lock.release()


def main():
    start_time = time.time()

    room_lock = mp.Lock()
    light_lock = mp.Lock()
    cleaning_signal = mp.Semaphore(0)  # Signal for cleaners to start cleaning
    stop_event = mp.Event()

    guest_count = mp.Value('i', 0)
    cleaned_count = mp.Value('i', 0)
    party_count = mp.Value('i', 0)

    cleaners = [
        mp.Process(target=cleaner, args=(room_lock, light_lock, cleaning_signal, stop_event, i, cleaned_count))
        for i in range(CLEANING_STAFF)
    ]
    guests = [
        mp.Process(target=guest, args=(room_lock, light_lock, cleaning_signal, guest_count, party_count, stop_event, i))
        for i in range(HOTEL_GUESTS)
    ]

    for c in cleaners:
        c.start()
    for g in guests:
        g.start()

    time.sleep(TIME)
    stop_event.set()

    for c in cleaners:
        c.join()
    for g in guests:
        g.join()

    print(f"\nRoom was cleaned {cleaned_count.value} times, there were {party_count.value} parties")


if __name__ == '__main__':
    main()