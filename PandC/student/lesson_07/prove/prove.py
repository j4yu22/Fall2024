"""
Course: CSE 251 
Lesson: L07 Prove
File:   prove.py
Author: Jay Underwood

Purpose: Process Task Files.

Instructions:

See Canvas for the full instructions for this assignment. You will need to complete the TODO comment
below before submitting this file:

Note: each of the 5 task functions need to return a string.  They should not print anything.

TODO:
I didn't select a constant for each pool size, I wrote code using the multiprocessing library to use the number of physical cores on the given machine
running the program - 1. I decided to do that after testing thoroughly, and finding that for both my desktop and laptop (both of which use hyperthreading)
a pool size of 5 was ideal for each pool, even after changing values such as lowering pool size for I/O bound processes like 'name'. Because of hyperthreading,
the multiprocessing library was picking up logical processors, not physical core count, which is why usable_cores is the number of logical processors divided by
2, then minus 1. I found that this dynamically optimized the pool size when ran on both my laptop and desktop.

Add your comments here on the pool sizes that you used for your assignment and why they were the best choices.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 
import multiprocessing as mp

# Include cse 251 common Python files - Dont change
from cse251 import *

# Constants - Don't change
TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# TODO: Change the pool sizes and explain your reasoning in the header comment
num_cores = mp.cpu_count()
usable_cores = max(1, math.ceil(num_cores / 2 - 1))
print(usable_cores, num_cores)

PRIME_POOL_SIZE = usable_cores
WORD_POOL_SIZE  = usable_cores
UPPER_POOL_SIZE = usable_cores
SUM_POOL_SIZE   = usable_cores
NAME_POOL_SIZE  = usable_cores

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
        return f"{value} is prime"
    else:
        return f"{value} is not prime"


def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt', 'r') as f:
        words = f.read().splitlines()
    if word in words:
        return f"{word} Found"
    else:
        return f"{word} not found *****"


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return f"{text} ==> {text.upper()}"

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of all numbers between start_value and end_value
        answer = {start_value:,} to {end_value:,} = {total:,}
    """
    total = sum(range(start_value, end_value + 1))
    return f"sum of all numbers from {start_value:,} to {end_value:,} = {total:,}"


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            name = response.json().get('name', 'Unknown')
            return f"{url} has name {name}"
        else:
            return f"{url} had an error receiving the information"
    except requests.RequestException:
        return f"{url} had an error receiving the information"


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    pool_prime = mp.Pool(PRIME_POOL_SIZE)
    pool_word = mp.Pool(WORD_POOL_SIZE)
    pool_upper = mp.Pool(UPPER_POOL_SIZE)
    pool_sum = mp.Pool(SUM_POOL_SIZE)
    pool_name = mp.Pool(NAME_POOL_SIZE)
    # TODO change the following if statements to start the pools
    
    count = 0
    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        task = load_json_file(filename)
        count += 1
        task_type = task['task']
        
        if task_type == TYPE_PRIME:
            pool_prime.apply_async(task_prime, args=(task['value'],), callback=lambda x: result_primes.append(x))
        elif task_type == TYPE_WORD:
            pool_word.apply_async(task_word, args=(task['word'],), callback=lambda x: result_words.append(x))
        elif task_type == TYPE_UPPER:
            pool_upper.apply_async(task_upper, args=(task['text'],), callback=lambda x: result_upper.append(x))
        elif task_type == TYPE_SUM:
            pool_sum.apply_async(task_sum, args=(task['start'], task['end']), callback=lambda x: result_sums.append(x))
        elif task_type == TYPE_NAME:
            pool_name.apply_async(task_name, args=(task['url'],), callback=lambda x: result_names.append(x))



    # TODO wait on the pools
    pool_prime.close()
    pool_word.close()
    pool_upper.close()
    pool_sum.close()
    pool_name.close()

    pool_prime.join()
    pool_word.join()
    pool_upper.join()
    pool_sum.join()
    pool_name.join()

    # DO NOT change any code below this line!
    #---------------------------------------------------------------------------
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Total time to process {count} tasks')


if __name__ == '__main__':
    main()