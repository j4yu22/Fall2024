def sub_list_sort(input_array):
    """
    Sorts the input array using a sub-list sorting algorithm.
    
    Parameters:
        input_array (list): The array to be sorted.
    
    Returns:
        list: The sorted array.
    """
    # If the array has only one element or is already sorted, return it as-is
    if len(input_array) <= 1 or is_sorted(input_array):
        return input_array

    n = len(input_array)
    destination_array = [0] * n  # Initialize with zeros to avoid output issues

    # Main loop until the array is fully sorted
    while not is_sorted(input_array):
        # Identify sorted sub-lists (runs)
        runs = identify_sorted_runs(input_array)
        # Clear the destination array before merging
        clear(destination_array)
        # Merge runs into the destination array
        merge_runs_into_destination(runs, destination_array)
        # Copy the sorted elements back to the input array
        copy(destination_array, input_array)

    return destination_array


def identify_sorted_runs(input_array):
    """
    Identifies sorted sub-lists (runs) within the input array.

    Parameters:
        input_array (list): The array to identify runs from.

    Returns:
        list: A list of sorted sub-lists (runs).
    """
    runs = []
    start_index = 0
    for i in range(1, len(input_array)):
        if input_array[i] < input_array[i - 1]:
            run = input_array[start_index:i]
            runs.append(run)
            start_index = i
    # Add the last run
    runs.append(input_array[start_index:])
    return runs


def merge_runs_into_destination(runs, destination_array):
    """
    Merges sorted runs into the destination array.

    Parameters:
        runs (list of lists): The sorted sub-lists to merge.
        destination_array (list): The array where the merged result will be stored.
    """
    dest_index = 0
    while runs:
        # Find the run with the smallest starting element
        smallest_run_index = find_run_with_smallest_element(runs)
        smallest_element = runs[smallest_run_index][0]
        destination_array[dest_index] = smallest_element
        dest_index += 1
        # Remove the used element from the current run
        runs[smallest_run_index].pop(0)
        if not runs[smallest_run_index]:  # If the run is empty, remove it
            runs.pop(smallest_run_index)


def find_run_with_smallest_element(runs):
    """
    Finds the index of the run with the smallest starting element.

    Parameters:
        runs (list of lists): The list of runs to search.

    Returns:
        int: The index of the run with the smallest starting element.
    """
    smallest_value = float('inf')
    smallest_run_index = -1
    for i in range(len(runs)):
        if runs[i][0] < smallest_value:
            smallest_value = runs[i][0]
            smallest_run_index = i
    return smallest_run_index


def copy(source_array, target_array):
    """
    Copies elements from the source array to the target array.

    Parameters:
        source_array (list): The array to copy from.
        target_array (list): The array to copy to.
    """
    for i in range(len(source_array)):
        target_array[i] = source_array[i]


def is_sorted(array):
    """
    Checks if the array is sorted in ascending order.

    Parameters:
        array (list): The array to check.

    Returns:
        bool: True if sorted, False otherwise.
    """
    for i in range(1, len(array)):
        if array[i] < array[i - 1]:
            return False
    return True


def clear(array):
    """
    Clears the array by setting all elements to zero.

    Parameters:
        array (list): The array to clear.
    """
    for i in range(len(array)):
        array[i] = 0
# Automation driver for testing and program trace
def test_sub_list_sort():
    test_cases = [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),  # Already sorted
        ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),  # Reverse order
        ([4, 2, 4, 3, 1, 4, 2, 1, 5], [1, 1, 2, 2, 3, 4, 4, 4, 5]),          # Mixed order with duplicates
        ([7], [7]),                                                          # Single element
        ([5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5]),                      # All elements the same
        ([8, 3, 1, 7, 4, 6, 2, 5], [1, 2, 3, 4, 5, 6, 7, 8]),                # Random unsorted
        ([], []),                                                            # Empty list
        ([-3, 7, -1, 5, 0, -2, 4], [-3, -2, -1, 0, 4, 5, 7])                 # List with negative and positive numbers
    ]

    for i, (input_array, expected_output) in enumerate(test_cases):
        print(f"Tracing Test Case {i + 1}")
        print(f"Initial Array: {input_array}")
        output = sub_list_sort(input_array.copy())
        print(f"Output: {output}")
        print(f"Expected: {expected_output}")
        print(f"Test Result: {'Passed' if output == expected_output else 'Failed'}")
        print("-" * 40)

# Run the test driver
if __name__ == "__main__":
    test_sub_list_sort()