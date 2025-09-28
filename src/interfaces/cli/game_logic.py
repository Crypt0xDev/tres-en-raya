import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from src.core.board import Board
from src.core.player import Player
from .ui.console_ui import ConsoleUI


def start_game():
    """Inicia un juego local de tres en raya"""
    ui = ConsoleUI()
    ui.display_welcome()

    # Crear jugadores
    player1 = Player("Jugador 1")
    player2 = Player("Jugador 2")
    player1.set_symbol("X")
    player2.set_symbol("O")

    players = [player1, player2]
    current_player_index = 0

    # Crear tablero
    board = Board()

    while True:
        ui.display_board(board.board)
        current_player = players[current_player_index]

        # Obtener movimiento del jugador
        position = ui.get_player_input(current_player.name)
        row, col = divmod(position, 3)

        # Realizar movimiento
        if make_move(board, current_player.symbol, row, col):
            # Verificar ganador
            winner = check_winner(board)
            if winner:
                ui.display_board(board.board)
                ui.display_winner(f"Jugador {winner}")
                break
            elif is_board_full(board):
                ui.display_board(board.board)
                ui.display_draw()
                break

            # Cambiar turno
            current_player_index = 1 - current_player_index
        else:
            print("Movimiento inválido. Intenta de nuevo.")


def check_winner(board):
    """Verifica si hay un ganador en el tablero"""
    return board.check_winner()


def make_move(board, player_symbol, row, col):
    """Realiza un movimiento en el tablero"""
    if board.board[row][col] == " ":
        board.board[row][col] = player_symbol
        return True
    return False


def is_board_full(board):
    """Verifica si el tablero está lleno"""
    return board.is_board_full()


def reset_game(board):
    """Reinicia el juego"""
    board.reset()
