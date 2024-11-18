"""
Course: CSE 251 
Lesson: L09 Prove Part 2
File:   prove_part_2.py
Author: Jay Underwood

Purpose: Part 2 of prove 9, finding the path to the end of a maze using recursion.

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- You MUST use recursive threading to find the end of the maze.
- Each thread MUST have a different color than the previous thread:
    - Use get_color() to get the color for each thread; you will eventually have duplicated colors.
    - Keep using the same color for each branch that a thread is exploring.
    - When you hit an intersection spin off new threads for each option and give them their own colors.

This code is not interested in tracking the path to the end position. Once you have completed this
program however, describe how you could alter the program to display the found path to the exit
position:

What would be your strategy?

I would modify the program to store each thread's moves in a path list. When a thread reaches
the maze's end, it should signal all other threads to stop and trace back the threads that got it to the end,
then print the stored path list as the solution.

Why would it work?

This approach works because each thread keeps track of its own path. When a thread reaches the exit, 
the stored path can be printed or returned, ensuring the complete path to the exit is recorded and displayed.

"""

import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


# TODO: Add any function(s) you need, if any, here.

def solve_find_end(maze):
    """ Solve the maze using recursive threading. Each branch uses a new thread at intersections. """
    global stop, thread_count
    stop = False
    thread_count = 0

    def depth_first(row, col, color):
        global stop, thread_count
        if stop:
            return

        # Check if the maze is already solved
        if maze.at_end(row, col):
            maze.move(row, col, color)
            stop = True
            return

        if not maze.can_move_here(row, col):
            return

        maze.move(row, col, color)

        possible_moves = maze.get_possible_moves(row, col)

        # If there's only one move, continue with the current thread
        if len(possible_moves) == 1:
            next_row, next_col = possible_moves[0]
            if maze.can_move_here(next_row, next_col):
                depth_first(next_row, next_col, color)
        else:
            # Create new threads for each move at intersections
            threads = []
            for i, (next_row, next_col) in enumerate(possible_moves):
                if maze.can_move_here(next_row, next_col) and not stop:
                    if i == 0:
                        new_color = color
                        thread = threading.Thread(target=depth_first, args=(next_row, next_col, new_color))
                        threads.append(thread)
                        thread_count += 1
                        thread.start()
                    else:
                        new_color = get_color()  # Each thread gets a different color
                        thread = threading.Thread(target=depth_first, args=(next_row, next_col, new_color))
                        threads.append(thread)
                        thread_count += 1
                        thread.start()

            for thread in threads:
                thread.join()

    start_row, start_col = maze.get_start_pos()
    initial_color = get_color()
    initial_thread = threading.Thread(target=depth_first, args=(start_row, start_col, initial_color))
    thread_count += 1
    initial_thread.start()
    initial_thread.join()


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True


def find_ends(log):
    """ Do not change this function """

    files = (
        ('very-small.bmp', True),
        ('very-small-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False),
        ('large-squares.bmp', False),
        ('large-open.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        filename = f'./mazes/{filename}'
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)


if __name__ == "__main__":
    main()