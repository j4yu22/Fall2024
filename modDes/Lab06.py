import json

# 1. Name:
#      Jay Underwood
# 2. Assignment Name:
#      Lab 06 : Sudoku Program
# 3. Assignment Description:
#      This program allows users to play Sudoku and enforces the game rules, including uniqueness in rows, columns, and 3x3 squares.
# 4. What was the hardest part? Be as specific as possible.
#      The hardest part was managing rule enforcement in the game, especially ensuring all three uniqueness checks (rows, columns, and squares) were done correctly.
# 5. How long did it take for you to complete the assignment?
#      4 hours

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


def get_board_coordinates(coord):
    """Convert user input coordinates to row and column indices."""
    if len(coord) == 2:
        if coord[0].isdigit():  # Handle "2B" case
            row, col = coord
        else:  # Handle "B2" case
            col, row = coord
    else:
        return None

    row_index = int(row) - 1
    col_index = ord(col.upper()) - ord('A')
    
    if 0 <= row_index < 9 and 0 <= col_index < 9:
        return row_index, col_index
    else:
        return None


def is_valid_move(board, row, col, value):
    """Check if the move is valid according to Sudoku rules."""
    # Check row uniqueness
    if value in board[row]:
        return False, "Number already exists in the row."
    
    # Check column uniqueness
    if value in [board[i][col] for i in range(9)]:
        return False, "Number already exists in the column."

    # Check 3x3 grid uniqueness
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == value:
                return False, "Number already exists in the 3x3 grid."

    return True, None


def edit_board(board, coord, value):
    """Edit the board at a given coordinate with a specified value."""
    coord_indices = get_board_coordinates(coord)
    if not coord_indices:
        print("Invalid coordinate. Please try again.")
        return

    row, col = coord_indices

    if board[row][col] != 0:
        print("This square is already filled. Please choose another.")
        return

    valid_move, error_message = is_valid_move(board, row, col, value)
    if not valid_move:
        print(error_message)
        return

    board[row][col] = value


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
        elif len(user_input) == 2 or len(user_input) == 3:
            value = input(f"What number goes in {user_input.upper()}? ")

            if value.isdigit() and 1 <= int(value) <= 9:
                edit_board(board, user_input, int(value))
            else:
                print("Invalid value. Please enter a number between 1 and 9.")
        else:
            print("Invalid input. Please enter a coordinate or 'Q' to quit.")


if __name__ == "__main__":
    main()
