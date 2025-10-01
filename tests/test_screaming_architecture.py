"""
Test básico para validar la estructura de Screaming Architecture.

Este test verifica que los componentes principales del dominio
funcionen correctamente y que los imports sean válidos.
"""

import unittest
import sys
from pathlib import Path

# Add project root to path for Screaming Architecture imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from game.entities.board import Board, CellState, Position, Move
from game.entities.player import Player, PlayerType, PlayerSymbol
from game.entities.game_session import GameSession, GameConfiguration


class TestScreamingArchitecture(unittest.TestCase):
    """Tests básicos para validar la estructura de Screaming Architecture."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.board = Board()
        self.player1 = Player(name="Test Player 1", player_type=PlayerType.HUMAN)
        self.player2 = Player(name="Test Player 2", player_type=PlayerType.AI_EASY)

    def test_board_creation(self):
        """Test que el board se crea correctamente."""
        self.assertIsInstance(self.board, Board)
        self.assertEqual(self.board.size, 3)

    def test_board_initial_state(self):
        """Test que el board inicializa en estado vacío."""
        for row in range(3):
            for col in range(3):
                position = Position(row, col)
                self.assertEqual(self.board.get_cell_state(position), CellState.EMPTY)

    def test_player_creation(self):
        """Test que los jugadores se crean correctamente."""
        self.assertIsInstance(self.player1, Player)
        self.assertEqual(self.player1.name, "Test Player 1")
        self.assertEqual(self.player1.player_type, PlayerType.HUMAN)
        
        self.assertIsInstance(self.player2, Player)
        self.assertEqual(self.player2.name, "Test Player 2")
        self.assertEqual(self.player2.player_type, PlayerType.AI_EASY)

    def test_board_place_move(self):
        """Test hacer movimientos en el tablero."""
        position = Position(0, 0)
        move = Move(position, CellState.PLAYER_X)
        
        # Test movimiento válido
        success = self.board.place_move(move)
        self.assertTrue(success)
        self.assertEqual(self.board.get_cell_state(position), CellState.PLAYER_X)
        
        # Test movimiento inválido (celda ocupada)
        move2 = Move(position, CellState.PLAYER_O)
        success = self.board.place_move(move2)
        self.assertFalse(success)
        self.assertEqual(self.board.get_cell_state(position), CellState.PLAYER_X)

    def test_board_empty_positions(self):
        """Test obtener posiciones vacías."""
        empty_positions = self.board.get_empty_positions()
        self.assertEqual(len(empty_positions), 9)  # Tablero 3x3 vacío
        
        # Hacer un movimiento
        position = Position(1, 1)
        move = Move(position, CellState.PLAYER_X)
        self.board.place_move(move)
        
        empty_positions = self.board.get_empty_positions()
        self.assertEqual(len(empty_positions), 8)
        self.assertNotIn(position, empty_positions)

    def test_game_session_creation(self):
        """Test creación de sesión de juego."""
        config = GameConfiguration()
        session = GameSession(config)
        
        self.assertIsInstance(session, GameSession)
        self.assertIsInstance(session.board, Board)

    def test_position_validation(self):
        """Test validación de posiciones."""
        # Posiciones válidas
        valid_positions = [
            Position(0, 0), Position(1, 1), Position(2, 2),
            Position(0, 1), Position(1, 0), Position(2, 1)
        ]
        
        for pos in valid_positions:
            self.assertTrue(self.board.is_position_empty(pos))

    def test_board_is_full(self):
        """Test verificar si el tablero está lleno."""
        self.assertFalse(self.board.is_full())
        
        # Llenar todo el tablero
        for row in range(3):
            for col in range(3):
                player = CellState.PLAYER_X if (row + col) % 2 == 0 else CellState.PLAYER_O
                move = Move(Position(row, col), player)
                self.board.place_move(move)
        
        self.assertTrue(self.board.is_full())


if __name__ == '__main__':
    unittest.main()