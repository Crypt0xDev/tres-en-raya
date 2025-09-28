def calculate_winner(board):
    # Check rows, columns, and diagonals for a winner
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != "":
            return row[0]

    for col in range(len(board)):
        if all(board[row][col] == board[0][col] and board[0][col] != "" for row in range(len(board))):
            return board[0][col]

    if all(board[i][i] == board[0][0] and board[0][0] != "" for i in range(len(board))):
        return board[0][0]

    if all(board[i][len(board) - 1 - i] == board[0][len(board) - 1] and board[0][len(board) - 1] != "" for i in range(len(board))):
        return board[0][len(board) - 1]

    return None


def is_board_full(board):
    return all(cell != "" for row in board for cell in row)


def reset_board(size):
    return [["" for _ in range(size)] for _ in range(size)]