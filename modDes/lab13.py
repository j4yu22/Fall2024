# 1. Name:
#      Jay Underwood
# 2. Assignment Name:
#      Lab 13 : Segregation Sort Program
# 3. Assignment Description:
#      This program implements the segregation sort algorithm, which reorders an input list
#      so that odd numbers appear first in sorted order, followed by even numbers in sorted order.
# 4. What was the hardest part? Be as specific as possible.
#      The hardest part was modifying the implementation to ensure both odd and even numbers
#      are sorted independently while preserving the general segregation logic.
# 5. How long did it take for you to complete the assignment?
#     About 3 hours.

def segregation_sort(arr):
    """
    Segregates and sorts an array by placing odd numbers first, followed by even numbers.
    Odd and even numbers are sorted in ascending order.

    Parameters:
        arr (list of int): The input list to be segregated and sorted.

    Returns:
        list of int: The segregated and sorted list.
    """
    # Separate the list into odd and even numbers, then sort each
    odd = sorted([x for x in arr if x % 2 != 0])
    even = sorted([x for x in arr if x % 2 == 0])
    # Merge the two lists
    return odd + even


def main():
    """
    Demonstrates the segregation_sort function with multiple test cases and prints results.
    """
    test_cases = [
        ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], "Test Case 1: Random Input"),
        ([1, 2, 3, 4, 5, 6], "Test Case 2: Already Sorted"),
        ([6, 5, 4, 3, 2, 1], "Test Case 3: Reverse Sorted"),
        ([42], "Test Case 4: Single Element"),
        ([], "Test Case 5: Empty Array"),
    ]

    for test, description in test_cases:
        result = segregation_sort(test)
        print(f"{description} -> Input: {test}, Output: {result}")


if __name__ == "__main__":
    main()