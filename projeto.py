from random import randrange

def display_board(board):
    """Display the board in the specified format."""
    print("+-------+-------+-------+")
    for row in range(3):
        print("|       |       |       |")
        print("|", end=" ")
        for col in range(3):
            print(f"  {board[row][col]}  ", end="|" if col < 2 else " ")
        print()
        print("|       |       |       |")
        print("+-------+-------+-------+")

def enter_move(board):
    """Get the user's move and update the board."""
    while True:
        try:
            move = int(input("Enter your move: "))
            if move < 1 or move > 9:
                print("Invalid input. Please enter a number between 1 and 9.")
                continue
            
            # Convert 1-9 to row, col (0-based)
            row = (move - 1) // 3
            col = (move - 1) % 3
            
            # Check if the square is free
            if board[row][col] in ['O', 'X']:
                print("That square is already occupied. Choose another.")
                continue
                
            board[row][col] = 'O'
            break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

def make_list_of_free_fields(board):
    """Return a list of tuples (row, col) for all free positions."""
    free_fields = []
    for row in range(3):
        for col in range(3):
            if board[row][col] not in ['O', 'X']:
                free_fields.append((row, col))
    return free_fields

def victory_for(board, sign):
    """Check if the player with the given sign has won."""
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == sign:
            return True
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == sign:
            return True
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == sign:
        return True
    if board[0][2] == board[1][1] == board[2][0] == sign:
        return True
    
    return False

def draw_move(board):
    """Make the computer's move (random choice)."""
    free_fields = make_list_of_free_fields(board)
    if free_fields:
        row, col = free_fields[randrange(len(free_fields))]
        board[row][col] = 'X'

# Initialize the board
board = [
    ['1', '2', '3'],
    ['4', 'X', '6'],  # Computer starts with X in the middle
    ['7', '8', '9']
]

# Game loop
while True:
    # Display current board
    display_board(board)
    
    # Check if computer won
    if victory_for(board, 'X'):
        print("Computer won!")
        break
    
    # Check if it's a tie
    if not make_list_of_free_fields(board):
        print("It's a tie!")
        break
    
    # User's turn
    enter_move(board)
    
    # Check if user won
    if victory_for(board, 'O'):
        display_board(board)
        print("You won!")
        break
    
    # Check if it's a tie after user's move
    if not make_list_of_free_fields(board):
        display_board(board)
        print("It's a tie!")
        break
    
    # Computer's turn
    draw_move(board)