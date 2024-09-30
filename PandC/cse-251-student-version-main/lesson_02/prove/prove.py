"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: Jay Underwood

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}

Outline of API calls to server

1) Use TOP_API_URL to get the dictionary above
2) Add "6" to the end of the films endpoint to get film 6 details
3) Use as many threads possible to get the names of film 6 data (people, starships, ...)

"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
# this import wasn't working
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

    # Create threads for each URL in the section
    for url in urls:
        thread = APIThread(url, section_name)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
        results.append(thread.result)

    return sorted(results)


def main():
    global call_count
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # Step 1: Retrieve Top API urls
    response = requests.get(TOP_API_URL)
    call_count += 1

    if response.status_code == 200:
        api_urls = response.json()
    else:
        print("Error retrieving top API URL")
        return

    # Step 2: Retrieve Details on film 6
    film_url = api_urls['films'] + "6"
    response = requests.get(film_url)
    call_count += 1

    if response.status_code == 200:
        film_data = response.json()
    else:
        print("Error retrieving film 6 data")
        return

    # Print film details
    print(f"\nTitle   : {film_data['title']}")
    print(f"Director: {film_data['director']}")
    print(f"Producer: {film_data['producer']}")
    print(f"Released: {film_data['release_date']}\n")

    # Step 3: Retrieve additional data using threads
    sections = ['characters', 'planets', 'starships', 'vehicles', 'species']
    for section in sections:
        urls = film_data[section]
        results = get_data_from_section(urls, section)

        # Display the section results
        print(f"{section.capitalize()}: {len(results)}")
        print(', '.join(results))
        print()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')


if __name__ == "__main__":
    main()
