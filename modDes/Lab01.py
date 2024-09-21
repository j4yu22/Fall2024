# 1. Name:
#      Jay Underwood
# 2. Assignment Name:
#      Lab 01: Tic-Tac-Toe
# 3. Assignment Description:
#      Play a game of Tic Tac Toe with a friend.
# 4. What was the hardest part? Be as specific as possible.
#      For me the hardest part was getting the board state to be able to be saved. It was tricky using the json and making sure it saved when the user quit.
#      Once I figured it out it was a lot easier to get the board to reset after the end of a game, wheter it was a tie, or a win for either side, but working with Json was probably the trickiest part.
# 5. How long did it take for you to complete the assignment?
#      It took me about an hour and 25 minutes to finish this.
import json

X = 'X'
O = 'O'
BLANK = ' '

blank_board = {  
    "board": [
        BLANK, BLANK, BLANK,
        BLANK, BLANK, BLANK,
        BLANK, BLANK, BLANK ]
}

def read_board(filename):
    '''Read the previously existing board from the file if it exists.'''
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data['board']
    except FileNotFoundError:
        return blank_board['board']

def save_board(filename, board):
    '''Save the current game to a file.'''
    with open(filename, 'w') as f:
        json.dump({"board": board}, f)

def display_board(board):
    '''Display a Tic-Tac-Toe board on the screen in a user-friendly way.'''
    for i in range(3):
        row = " | ".join(board[i*3:(i+1)*3])
        print(f" {row} ")
        if i < 2:
            print("---+---+---")

def is_x_turn(board):
    '''Determine whose turn it is.'''
    x_count = board.count(X)
    o_count = board.count(O)
    return x_count == o_count

def play_game(board):
    '''Play the game of Tic-Tac-Toe.'''
    while True:
        display_board(board)
        
        if is_x_turn(board):
            player = X
        else:
            player = O
        print(f"{player}'s turn. Enter a number (1-9) or 'q' to quit:")
        
        move = input(f"{player}> ").strip()
        
        if move.lower() == 'q':
            save_board('tictactoe.json', board)
            print("Game saved. Exiting...")
            return False

        if move.isdigit() and 1 <= int(move) <= 9:
            position = int(move) - 1
            if board[position] == BLANK:
                board[position] = player
            else:
                print("That position is already taken. Try again.")
                continue
        else:
            print("Invalid input. Try again.")
            continue
        
        if game_done(board, message=True):
            print("Resetting the board for a new game...\n")
            board[:] = blank_board['board']
            return True


def game_done(board, message=False):
    '''Determine if the game is finished.
       Note that this function is provided as-is.
       You do not need to edit it in any way.
       If message == True, then we display a message to the user.
       Otherwise, no message is displayed. '''

    for row in range(3):
        if board[row * 3] != BLANK and board[row * 3] == board[row * 3 + 1] == board[row * 3 + 2]:
            if message:
                print("The game was won by", board[row * 3])
            return True

    for col in range(3):
        if board[col] != BLANK and board[col] == board[3 + col] == board[6 + col]:
            if message:
                print("The game was won by", board[col])
            return True

    if board[4] != BLANK and (board[0] == board[4] == board[8] or
                              board[2] == board[4] == board[6]):
        if message:
            print("The game was won by", board[4])
        return True

    tie = True
    for square in board:
        if square == BLANK:
            tie = False
    if tie:
        if message:
            print("The game is a tie!")
        return True

    return False

print("Enter 'q' to suspend your game. Otherwise, enter a number from 1 to 9")
print("where the following numbers correspond to the locations on the grid:")
print(" 1 | 2 | 3 ")
print("---+---+---")
print(" 4 | 5 | 6 ")
print("---+---+---")
print(" 7 | 8 | 9 \n")
print("The current board is:")

if __name__ == "__main__":
    board = read_board('tictactoe.json')

    while play_game(board):
        print("Starting a new game...")
