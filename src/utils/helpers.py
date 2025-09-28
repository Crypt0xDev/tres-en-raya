"""
Utility functions for Tic-Tac-Toe game operations.

This module provides helper functions for common game operations such as
winner calculation, board status checking, and board initialization.
These functions are designed to work with boards of any square size.
"""


def calculate_winner(board):
    """
    Determine if there is a winner on the given board.
    
    Checks all possible winning combinations on a square board of any size:
    - All rows (horizontal wins)
    - All columns (vertical wins)
    - Main diagonal (top-left to bottom-right)
    - Anti-diagonal (top-right to bottom-left)
    
    Args:
        board (list): A 2D list representing the game board where empty cells
                     are represented by empty strings ("") and filled cells
                     contain player marks (e.g., "X", "O")
    
    Returns:
        str or None: The winning player's mark if a winner exists,
                    None if no winner is found
    
    Example:
        >>> board = [["X", "X", "X"], ["O", "O", ""], ["", "", ""]]
        >>> calculate_winner(board)
        'X'
    """
    # Check rows for winner
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != "":
            return row[0]

    # Check columns for winner
    for col in range(len(board)):
        if all(
            board[row][col] == board[0][col] and board[0][col] != ""
            for row in range(len(board))
        ):
            return board[0][col]

    # Check main diagonal (top-left to bottom-right)
    if all(board[i][i] == board[0][0] and board[0][0] != "" for i in range(len(board))):
        return board[0][0]

    # Check anti-diagonal (top-right to bottom-left)
    if all(
        board[i][len(board) - 1 - i] == board[0][len(board) - 1]
        and board[0][len(board) - 1] != ""
        for i in range(len(board))
    ):
        return board[0][len(board) - 1]

    return None


def is_board_full(board):
    """
    Check if the game board is completely filled.
    
    Examines every cell on the board to determine if all positions
    have been filled by players (no empty cells remain).
    
    Args:
        board (list): A 2D list representing the game board where empty cells
                     are represented by empty strings ("")
    
    Returns:
        bool: True if all cells are filled, False if any empty cell exists
    
    Example:
        >>> board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
        >>> is_board_full(board)
        True
        >>> board = [["X", "O", ""], ["O", "X", "O"], ["O", "X", "O"]]
        >>> is_board_full(board)
        False
    """
    return all(cell != "" for row in board for cell in row)


def reset_board(size):
    """
    Create a new empty game board of the specified size.
    
    Generates a square board (size x size) with all cells initialized
    to empty strings, ready for a new game.
    
    Args:
        size (int): The dimension of the square board (must be positive)
    
    Returns:
        list: A 2D list of empty strings representing an empty board
    
    Raises:
        ValueError: If size is not a positive integer
    
    Example:
        >>> reset_board(3)
        [['', '', ''], ['', '', ''], ['', '', '']]
        >>> reset_board(4)
        [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    """
    if not isinstance(size, int) or size <= 0:
        raise ValueError("Board size must be a positive integer")
    
    return [["" for _ in range(size)] for _ in range(size)]
