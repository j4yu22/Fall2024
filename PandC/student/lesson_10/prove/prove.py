"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Jay Underwood

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can NOT use sleep() statements.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable from the buffer>, end=', ', flush=True)

Add any comments for me: N/A

"""

import random
import multiprocessing as mp
from multiprocessing.managers import SharedMemoryManager
from multiprocessing import Semaphore, Lock
from multiprocessing.shared_memory import ShareableList

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2


def writer(shared_list, write_semaphore, read_semaphore, write_lock, items_to_send):
    """
    Writer process: Writes items into the shared buffer.

    Parameters:
        shared_list (ShareableList): The shared buffer.
        write_semaphore (Semaphore): Semaphore to manage write operations.
        read_semaphore (Semaphore): Semaphore to signal readers.
        write_lock (Lock): Lock to ensure thread-safe writes.
        items_to_send (int): Number of items to write to the buffer.

    Returns:
        None
    """
    buffer_size = BUFFER_SIZE

    for _ in range(items_to_send):
        write_semaphore.acquire()
        with write_lock:
            write_index = shared_list[BUFFER_SIZE]
            current_value = shared_list[BUFFER_SIZE + 2]
            shared_list[write_index] = current_value
            shared_list[BUFFER_SIZE] = (write_index + 1) % buffer_size
            shared_list[BUFFER_SIZE + 2] += 1
        read_semaphore.release()

    for _ in range(READERS):
        read_semaphore.release()


def reader(shared_list, write_semaphore, read_semaphore, read_lock, received_count, total_items):
    """
    Reader process: Reads items from the shared buffer.

    Parameters:
        shared_list (ShareableList): The shared buffer.
        write_semaphore (Semaphore): Semaphore to signal writers.
        read_semaphore (Semaphore): Semaphore to manage read operations.
        read_lock (Lock): Lock to ensure thread-safe reads.
        received_count (Value): Shared counter to track received items.
        total_items (int): Total number of items to read.

    Returns:
        None
    """
    buffer_size = BUFFER_SIZE

    while True:
        read_semaphore.acquire()
        with read_lock:
            if received_count.value >= total_items:
                return
            read_index = shared_list[BUFFER_SIZE + 1]
            value = shared_list[read_index]
            received_count.value += 1
            if received_count.value == total_items:
                print(total_items, end="\n", flush=True)
                return
            else:
                print(value, end=", ", flush=True)
            shared_list[BUFFER_SIZE + 1] = (read_index + 1) % buffer_size
        write_semaphore.release()


def main():
    """
    Main function to set up shared memory and processes.

    Parameters:
        None

    Returns:
        None
    """
    items_to_send = random.randint(1000, 10000)
    smm = SharedMemoryManager()
    smm.start()
    shared_list = ShareableList([0] * BUFFER_SIZE + [0, 0, 1])
    write_semaphore = mp.Semaphore(BUFFER_SIZE)
    read_semaphore = mp.Semaphore(0)
    write_lock = mp.Lock()
    read_lock = mp.Lock()
    received_count = mp.Value('i', 0)
    writer_processes = [mp.Process(target=writer, args=(shared_list, write_semaphore, read_semaphore, write_lock, items_to_send // WRITERS)) for _ in range(WRITERS)]
    reader_processes = [mp.Process(target=reader, args=(shared_list, write_semaphore, read_semaphore, read_lock, received_count, items_to_send)) for _ in range(READERS)]

    for wp in writer_processes:
        wp.start()
    for rp in reader_processes:
        rp.start()

    for wp in writer_processes:
        wp.join()
    for rp in reader_processes:
        rp.join()

    print(f"\n{items_to_send} values sent")
    print(f"{received_count.value} values received")
    smm.shutdown()


if __name__ == '__main__':
    main()
