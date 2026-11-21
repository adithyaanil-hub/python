# Tic Tac Toe Game
# Two Player Game

def display_board(board):

    print("\n")

    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")

    print("\n")


# Function to check winner
def check_winner(board, player):

    winning_positions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for position in winning_positions:

        if (board[position[0]] == player and
            board[position[1]] == player and
                board[position[2]] == player):

            return True

    return False


# Function to play the game
def play_game():

    board = [" "] * 9

    current_player = "X"

    print("\n===== TIC TAC TOE GAME =====")

    print("Player 1: X")
    print("Player 2: O")

    print("\nBoard Positions:")

    print(" 1 | 2 | 3 ")
    print("---|---|---")
    print(" 4 | 5 | 6 ")
    print("---|---|---")
    print(" 7 | 8 | 9 ")

    while True:

        display_board(board)

        print("Player", current_player, "turn")

        choice = input("Enter position (1-9): ").strip()

        # Check empty input
        if choice == "":
            print("Input cannot be empty! Try again.")
            continue

        # Check numeric input
        try:
            position = int(choice)

        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        # Check position range
        if position < 1 or position > 9:
            print("Invalid position! Enter between 1 and 9.")
            continue

        # Check occupied position
        if board[position - 1] != " ":
            print("Position already occupied! Try again.")
            continue

        # Place player's mark
        board[position - 1] = current_player

        # Check winner
        if check_winner(board, current_player):

            display_board(board)

            print("Congratulations!")
            print("Player", current_player, "WINS!")

            break

        # Check draw
        if " " not in board:

            display_board(board)

            print("Game Draw!")

            break

        # Switch player
        if current_player == "X":
            current_player = "O"

        else:
            current_player = "X"


# Main program
while True:

    play_game()

    again = input("Do you want to play again? (yes/no): ").strip().lower()

    if again == "yes" or again == "y":
        continue

    elif again == "no" or again == "n":
        print("\nThank you for playing Tic Tac Toe!")
        break

    else:
        print("Invalid choice. Exiting game.")
        break
