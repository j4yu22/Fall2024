import json

# 1. Name:
#      Jay Underwood
# 2. Assignment Name:
#      Lab 05 : Sudoku Draft
# 3. Assignment Description:
#      This program allows a user to play Sudoku without enforcing rules. Users can
#      input any number into a specified cell, save the game, and reload it with changes.
# 4. What was the hardest part? Be as specific as possible.
#      The hardest part was managing file reading/writing while ensuring the board
#      maintains the correct format. Handling user inputs and converting them to the correct
#      board positions also required careful implementation.
# 5. How long did it take for you to complete the assignment?
#      3 and a half hours

def load_board(filename):
    """Load the Sudoku board from a JSON file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data['board']
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None


def save_board(filename, board):
    """Save the current board to a JSON file."""
    try:
        with open(filename, 'w') as file:
            json.dump({"board": board}, file)
            print(f"Board saved to {filename}.")
    except Exception as e:
        print(f"Error saving board: {e}")


def display_board(board):
    """Display the Sudoku board in a user-friendly format."""
    print("   A B C D E F G H I")
    for i, row in enumerate(board):
        row_display = ' '.join(str(num) if num != 0 else ' ' for num in row)
        print(f"{i + 1}  {row_display[:5]}|{row_display[6:11]}|{row_display[12:]}")
        if i == 2 or i == 5:
            print("   -----+-----+-----")


def edit_board(board, coord, value):
    """Edit the board at a given coordinate with a specified value."""
    column, row = coord[0].upper(), coord[1]
    col_index = ord(column) - ord('A')
    row_index = int(row) - 1

    if 0 <= col_index < 9 and 0 <= row_index < 9:
        board[row_index][col_index] = value
    else:
        print("Invalid coordinate. Please try again.")


def main():
    filename = input("Please input the file name of your board: ")
    board = load_board(filename)

    if not board:
        return

    while True:
        display_board(board)
        user_input = input("Specify a coordinate to edit or 'Q' to save and quit\n> ")

        if user_input.lower() == 'q':
            save_board(filename, board)
            break
        elif len(user_input) == 2 and user_input[0].isalpha() and user_input[1].isdigit():
            value = input(f"What number goes in {user_input.upper()}? ")

            if value.isdigit() and 1 <= int(value) <= 9:
                edit_board(board, user_input, int(value))
            else:
                print("Invalid value. Please enter a number between 1 and 9.")
        else:
            print("Invalid input. Please enter a coordinate or 'Q' to quit.")


if __name__ == "__main__":
    main()
