"""
Course: CSE 251, week 14
File: functions.py
Author: Jay Underwood

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family_id = 6128784944
request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
person_id = 2373686152
request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

To speed up part 1, the existing code can be optimized by reducing redundant work and improving concurrency. First, increasing the 
number of worker threads in the ThreadPoolExecutor allows for more family and person requests to be processed in parallel, better 
utilizing system resources. Second, eliminating duplicate API calls by carefully tracking visited families and added people with sets 
will ensure no unnecessary requests are made. Lastly, combining family and person requests more efficiently—such as fetching all family 
members before diving into child families—will minimize delays caused by thread idle time and API latency.

Describe how to speed up part 2

To speed up part 2, the code can leverage parallelism more effectively. By processing multiple families level by level using a larger 
thread pool, more family data can be retrieved simultaneously. Additionally, fetching all person data for a given level in parallel, 
rather than sequentially, reduces waiting time and improves throughput. Ensuring minimal overhead for thread management and keeping 
track of visited families will prevent unnecessary requests and allow the algorithm to progress smoothly through all levels of the search.


Extra (Optional) 10% Bonus to speed up part 3

To speed up part 3, aside from the already listed ways to speed up part 2, the most apparent would be not restricting the thread pool size to
just 5. The average times to run part 2 were around 6 to 7 seconds, and the average times for part 3 were around 40 seconds, which is a
massive difference.

"""
from common import *
import queue
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed

# -----------------------------------------------------------------------------
def depth_fs_pedigree(start_family_id, tree):
    """
    Optimized Depth-First Search for building the pedigree tree using ThreadPoolExecutor and a queue.
        
    Parameters:
        start_family_id (int): Starting family ID.
        tree (Tree): Tree object to store family and person data.
    """
    visited = set()
    added_people = set()
    task_queue = Queue()

    task_queue.put(start_family_id)
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []

        def process_family(family_id):
            """Process a single family and fetch related people."""
            if family_id in visited:
                return
            visited.add(family_id)

            request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
            request.start()
            request.join()
            family = request.get_response()

            if not family:
                print(f"Error: Family data for {family_id} could not be retrieved.")
                return

            print(f"Retrieved family: {family}")
            tree.add_family(Family(family))

            member_ids = [family.get('husband_id'), family.get('wife_id')] + family.get('children', [])
            for person_id in filter(None, member_ids):
                if person_id not in added_people:
                    added_people.add(person_id)
                    person_request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
                    person_request.start()
                    person_request.join()
                    person_data = person_request.get_response()

                    if person_data:
                        person = Person(person_data)
                        tree.add_person(person)

            for child_id in family.get('children', []):
                if child_id not in visited:
                    task_queue.put(child_id)

        while not task_queue.empty() or any(futures):
            while not task_queue.empty():
                family_id = task_queue.get()
                futures.append(executor.submit(process_family, family_id))

            completed = []
            for future in as_completed(futures):
                family_data = future.result()
                completed.append(future)
                if family_data:
                    for child_id in family_data.get('children', []):
                        if child_id not in visited:
                            task_queue.put(child_id)
                            visited.add(child_id)

            for future in completed:
                futures.remove(future)

    print("Depth-First Search completed.")

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_family_id, tree):
    """
    Breadth-First Search (BFS) for retrieving family tree data.
    Processes families level by level using a queue and concurrent threads.

    Parameters:
        start_family_id (int): Starting family ID.
        tree (Tree): Tree object to store family and person data.
    """
    # Use a set for visited families and people
    visited_families = set()
    added_people = set()
    family_queue = Queue()  # Queue to simulate BFS behavior

    family_queue.put(start_family_id)
    visited_families.add(start_family_id)

    with ThreadPoolExecutor(max_workers=50) as executor:
        while not family_queue.empty():
            current_families = []

            # Collect families at the current BFS level
            while not family_queue.empty():
                current_families.append(family_queue.get())

            future_families = []
            people_data = []

            def fetch_family(fam_id):
                """Fetch and process a single family."""
                request = Request_thread(f'{TOP_API_URL}/family/{fam_id}')
                request.start()
                request.join()
                family = request.get_response()

                if family:
                    tree.add_family(Family(family))
                    # Collect all member IDs
                    for member_id in [family.get('husband_id'), family.get('wife_id')] + family.get('children', []):
                        if member_id and member_id not in added_people:
                            people_data.append(member_id)
                            added_people.add(member_id)
                    # Add children to the queue for next BFS level
                    for child_id in family.get('children', []):
                        if child_id not in visited_families:
                            family_queue.put(child_id)
                            visited_families.add(child_id)

            # Fetch all families in the current level
            for fam_id in current_families:
                future_families.append(executor.submit(fetch_family, fam_id))

            for future in future_families:
                future.result()

            # Fetch all people concurrently at this level
            def fetch_person(person_id):
                person_request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
                person_request.start()
                person_request.join()
                person_data = person_request.get_response()
                if person_data:
                    tree.add_person(Person(person_data))

            futures_people = [executor.submit(fetch_person, pid) for pid in people_data]
            for future in futures_people:
                future.result()

    print("Breadth-First Search (BFS) completed.")

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_family_id, tree):
    """
    Breadth-First Search (BFS) for retrieving family tree data.
    Processes families level by level using a queue and concurrent threads.

    Parameters:
        start_family_id (int): Starting family ID.
        tree (Tree): Tree object to store family and person data.
    """
    # Use a set for visited families and people
    visited_families = set()
    added_people = set()
    family_queue = Queue()  # Queue to simulate BFS behavior

    family_queue.put(start_family_id)
    visited_families.add(start_family_id)
    
    # Thread count limited to 5
    with ThreadPoolExecutor(max_workers=5) as executor:
        while not family_queue.empty():
            current_families = []

            # Collect families at the current BFS level
            while not family_queue.empty():
                current_families.append(family_queue.get())

            future_families = []
            people_data = []

            def fetch_family(fam_id):
                """Fetch and process a single family."""
                request = Request_thread(f'{TOP_API_URL}/family/{fam_id}')
                request.start()
                request.join()
                family = request.get_response()

                if family:
                    tree.add_family(Family(family))
                    # Collect all member IDs
                    for member_id in [family.get('husband_id'), family.get('wife_id')] + family.get('children', []):
                        if member_id and member_id not in added_people:
                            people_data.append(member_id)
                            added_people.add(member_id)
                    # Add children to the queue for next BFS level
                    for child_id in family.get('children', []):
                        if child_id not in visited_families:
                            family_queue.put(child_id)
                            visited_families.add(child_id)

            # Fetch all families in the current level
            for fam_id in current_families:
                future_families.append(executor.submit(fetch_family, fam_id))

            for future in future_families:
                future.result()

            # Fetch all people concurrently at this level
            def fetch_person(person_id):
                person_request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
                person_request.start()
                person_request.join()
                person_data = person_request.get_response()
                if person_data:
                    tree.add_person(Person(person_data))

            futures_people = [executor.submit(fetch_person, pid) for pid in people_data]
            for future in futures_people:
                future.result()

    print("Breadth-First Search (BFS) completed.")