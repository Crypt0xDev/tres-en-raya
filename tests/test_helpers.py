"""
Tests para funciones auxiliares del dominio Tres en Raya.
Actualizado para Screaming Architecture.
"""

import os
import sys
import unittest
from pathlib import Path

# Add project root to path for Screaming Architecture imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from game.entities.board import Board, Position, Move, CellState


class TestBoardHelpers(unittest.TestCase):
    """Tests para funciones auxiliares del tablero."""

    def test_winner_row_first_row(self):
        """Test ganador en primera fila"""
        board = Board()
        # Crear línea horizontal X X X en primera fila
        for col in range(3):
            position = Position(0, col)
            move = Move(position, CellState.PLAYER_X)
            board.place_move(move)
        
        winner = board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_X)

    def test_winner_column_first_column(self):
        """Test ganador en primera columna"""
        board = Board()
        # Crear línea vertical O O O en primera columna
        for row in range(3):
            position = Position(row, 0)
            move = Move(position, CellState.PLAYER_O)
            board.place_move(move)
        
        winner = board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_O)

    def test_winner_main_diagonal(self):
        """Test ganador en diagonal principal"""
        board = Board()
        # Crear línea diagonal X X X
        for i in range(3):
            position = Position(i, i)
            move = Move(position, CellState.PLAYER_X)
            board.place_move(move)
        
        winner = board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_X)

    def test_winner_anti_diagonal(self):
        """Test ganador en diagonal secundaria"""
        board = Board()
        # Crear línea diagonal O O O (anti-diagonal)
        positions = [(0, 2), (1, 1), (2, 0)]
        for row, col in positions:
            position = Position(row, col)
            move = Move(position, CellState.PLAYER_O)
            board.place_move(move)
        
        winner = board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_O)

    def test_no_winner_empty_board(self):
        """Test sin ganador en tablero vacío"""
        board = Board()
        winner = board.get_winner()
        self.assertIsNone(winner)

    def test_no_winner_incomplete_game(self):
        """Test sin ganador en juego incompleto"""
        board = Board()
        moves = [(0, 0, CellState.PLAYER_X), (0, 1, CellState.PLAYER_O), (1, 1, CellState.PLAYER_X)]
        
        for row, col, player in moves:
            position = Position(row, col)
            move = Move(position, player)
            board.place_move(move)
        
        winner = board.get_winner()
        self.assertIsNone(winner)

    def test_board_full_detection(self):
        """Test detección de tablero lleno"""
        board = Board()
        
        # Llenar tablero completamente sin ganador: X O X / O X O / O X O
        moves = [
            (0, 0, CellState.PLAYER_X), (0, 1, CellState.PLAYER_O), (0, 2, CellState.PLAYER_X),
            (1, 0, CellState.PLAYER_O), (1, 1, CellState.PLAYER_X), (1, 2, CellState.PLAYER_O),
            (2, 0, CellState.PLAYER_O), (2, 1, CellState.PLAYER_X), (2, 2, CellState.PLAYER_O)
        ]
        
        for row, col, player in moves:
            position = Position(row, col)
            move = Move(position, player)
            board.place_move(move)
        
        self.assertTrue(board.is_full())
        self.assertIsNone(board.get_winner())  # No hay ganador - empate

    def test_board_not_full_partially_filled(self):
        """Test tablero no lleno cuando está parcialmente lleno"""
        board = Board()
        
        # Colocar algunos movimientos pero no llenar
        moves = [(0, 0, CellState.PLAYER_X), (0, 1, CellState.PLAYER_O)]
        for row, col, player in moves:
            position = Position(row, col)
            move = Move(position, player)
            board.place_move(move)
        
        self.assertFalse(board.is_full())

    def test_invalid_move_occupied_position(self):
        """Test movimiento inválido en posición ocupada"""
        board = Board()
        
        # Colocar primer movimiento
        position = Position(0, 0)
        move1 = Move(position, CellState.PLAYER_X)
        result1 = board.place_move(move1)
        self.assertTrue(result1)
        
        # Intentar colocar en la misma posición
        move2 = Move(position, CellState.PLAYER_O)
        result2 = board.place_move(move2)
        self.assertFalse(result2)

    def test_position_validation(self):
        """Test validación de posiciones"""
        board = Board()
        
        # Posición válida
        valid_position = Position(1, 1)
        self.assertTrue(board.is_position_empty(valid_position))
        
        # Colocar movimiento y verificar que ya no está vacía
        move = Move(valid_position, CellState.PLAYER_X)
        board.place_move(move)
        self.assertFalse(board.is_position_empty(valid_position))

    def test_board_state_consistency(self):
        """Test consistencia del estado del tablero"""
        board = Board()
        
        # Estado inicial - todas las celdas vacías
        for row in range(board.size):
            for col in range(board.size):
                position = Position(row, col)
                self.assertEqual(board.get_cell_state(position), CellState.EMPTY)
        
        # Después de movimientos
        position = Position(1, 1)
        move = Move(position, CellState.PLAYER_X)
        board.place_move(move)
        
        # Verificar que solo esa celda cambió
        self.assertEqual(board.get_cell_state(position), CellState.PLAYER_X)
        
        # Otras celdas siguen vacías
        other_position = Position(0, 0)
        self.assertEqual(board.get_cell_state(other_position), CellState.EMPTY)


if __name__ == "__main__":
    unittest.main()