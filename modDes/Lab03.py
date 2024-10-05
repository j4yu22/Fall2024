# 1. Name:
#      Jay Underwood
# 2. Assignment Name:
#      Lab 03: Calendar
# 3. Assignment Description:
#      This program generates a calendar for any given month and year, calculating the day of the week for the 1st day of the month and accounting for leap years.
# 4. What was the hardest part? Be as specific as possible.
#      The hardest part was figuring out the number of days from January 1, 1753, to the given date without using Python's datetime library. Implementing the leap years required careful handling of edge cases like non-leap century years.
# 5. How long did it take for you to complete the assignment?
#      About 4-5 hours including reading the instructions, recalling back to my charts and diagrams, and writing the program.

def is_leap_year(year):
    """
    Returns True if the given year is a leap year.
    A leap year is divisible by 4 but not by 100, unless also divisible by 400.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def number_days_in_month(month, year):
    """
    Returns the number of days in the given month and year.
    """
    if month == 1:
        return 31
    elif month == 2:
        return 29 if is_leap_year(year) else 28
    elif month == 3:
        return 31
    elif month == 4:
        return 30
    elif month == 5:
        return 31
    elif month == 6:
        return 30
    elif month == 7:
        return 31
    elif month == 8:
        return 31
    elif month == 9:
        return 30
    elif month == 10:
        return 31
    elif month == 11:
        return 30
    elif month == 12:
        return 31
    else:
        return 0


def compute_offset(month, year):
    """
    Returns the offset (day of the week) for the 1st of the given month and year.
    Offset is the number of days from Monday (0) to Sunday (6).
    January 1, 1753, was a Monday.
    """
    total_days = 0
    
    for y in range(1753, year):
        total_days += 366 if is_leap_year(y) else 365

    for m in range(1, month):
        total_days += number_days_in_month(m, year)

    return (total_days + 1) % 7


def display_table(num_days, dow):
    """
    Displays the calendar for the given month (num_days) starting on the given day of the week (dow).
    """
    print('  Su  Mo  Tu  We  Th  Fr  Sa')

    for _ in range(dow):
        print('    ', end='')

    for day in range(1, num_days + 1):
        print(f'{day:4}', end='')
        dow += 1
        if dow % 7 == 0:
            print()

    if dow % 7 != 0:
        print()


def main():
    """
    Main program function. Prompts the user for a month and year, and displays the calendar for that month.
    """
    while True:
        try:
            month = int(input("Enter the month number: "))
            if month < 1 or month > 12:
                print("Month must be between 1 and 12.")
            else:
                break
        except ValueError:
            print("Month must be an integer.")
    
    while True:
        try:
            year = int(input("Enter year: "))
            if year < 1753:
                print("Year must be 1753 or later.")
            else:
                break
        except ValueError:
            print("Year must be an integer.")

    days_in_month = number_days_in_month(month, year)
    offset = compute_offset(month, year)
    
    display_table(days_in_month, offset)


if __name__ == "__main__":
    main()
