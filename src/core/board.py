"""
Board module for Tic-Tac-Toe game.

This module contains the Board class that handles the game board state,
move validation, winner detection, and board display functionality.
"""


class Board:
    """
    Represents a Tic-Tac-Toe game board.
    
    The board is a 3x3 grid where players can place their marks ('X' or 'O').
    This class handles all board operations including move validation,
    winner detection, and game state management.
    
    Attributes:
        board (list): A 3x3 matrix representing the game board
        current_player (str): The player whose turn it is ('X' or 'O')
    """
    
    def __init__(self):
        """
        Initialize a new empty board.
        
        Creates a 3x3 grid filled with spaces and sets 'X' as the first player.
        """
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def display(self):
        """
        Display the current board state to console.
        
        Prints the board in a formatted grid with separators between rows.
        Each row shows the current state of the cells with '|' separators.
        """
        for row in self.board:
            print("|".join(row))
            print("-" * 5)

    def make_move(self, row, col):
        """
        Attempt to make a move at the specified position.
        
        Args:
            row (int): The row index (0-2)
            col (int): The column index (0-2)
        
        Returns:
            bool: True if the move was successful, False if the position is occupied
        
        Side Effects:
            - Updates the board with the current player's mark
            - Switches to the next player if move is successful
        """
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        """
        Check if there is a winner on the current board.
        
        Examines all possible winning combinations:
        - All rows (horizontal wins)
        - All columns (vertical wins) 
        - Both diagonals (diagonal wins)
        
        Returns:
            str or None: The winning player ('X' or 'O'), or None if no winner
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return row[0]

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                return self.board[0][col]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]

        return None

    def is_board_full(self):
        """Check if the board is full (draw condition)"""
        for row in self.board:
            for cell in row:
                if cell == " ":
                    return False
        return True

    def reset(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
