"""
Course: CSE 251 
Lesson: L07 Team
File:   team.py
Author: =Jay Underwood

Purpose: Retrieve Star Wars details from a server.

Instructions:

1) Make a copy of your lesson 2 prove assignment. Since you are  working in a team for this
   assignment, you can decide which assignment 2 program that you will use for the team activity.

2) You can continue to use the Request_Thread() class that makes the call to the server.

3) Convert the program to use a process pool that uses apply_async() with callback function(s) to
   retrieve data from the Star Wars website. Each request for data must be a apply_async() call;
   this means 1 url = 1 apply_async call, 94 urls = 94 apply_async calls.
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
# this import wasn't working on my desktop for some reason
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0

class APIThread(threading.Thread):
    def __init__(self, url, section):
        threading.Thread.__init__(self)
        self.url = url
        self.section = section
        self.result = None

    def run(self):
        global call_count
        response = requests.get(self.url)
        call_count += 1
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                self.result = data.get("name", "Unknown")
            else:
                self.result = data
        else:
            self.result = "Unknown"


def get_data_from_section(urls, section_name):
    threads = []
    results = []

    for url in urls:
        thread = APIThread(url, section_name)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        results.append(thread.result)

    return sorted(results)


def main():
    global call_count
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    response = requests.get(TOP_API_URL)
    call_count += 1

    if response.status_code == 200:
        api_urls = response.json()
    else:
        print("Error retrieving top API URL")
        return

    film_url = api_urls['films'] + "6"
    response = requests.get(film_url)
    call_count += 1

    if response.status_code == 200:
        film_data = response.json()
    else:
        print("Error retrieving film 6 data")
        return

    print(f"\nTitle   : {film_data['title']}")
    print(f"Director: {film_data['director']}")
    print(f"Producer: {film_data['producer']}")
    print(f"Released: {film_data['release_date']}\n")

    sections = ['characters', 'planets', 'starships', 'vehicles', 'species']
    for section in sections:
        urls = film_data[section]
        results = get_data_from_section(urls, section)

        print(f"{section.capitalize()}: {len(results)}")
        print(', '.join(results))
        print()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')


if __name__ == "__main__":
    main()
