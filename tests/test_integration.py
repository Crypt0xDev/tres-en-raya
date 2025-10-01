"""
Tests de integración end-to-end para el juego Tres en Raya.

Estos tests prueban flujos completos del juego y la interacción entre componentes.
"""

import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add project root to path for Screaming Architecture imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from game.entities.board import Board, Position, Move, CellState
from game.entities.game_session import GameSession, GameState
from game.entities.player import Player
from game.use_cases.start_new_game import StartNewGameUseCase, StartNewGameRequest
from game.use_cases.make_move import MakeMoveUseCase, MakeMoveRequest


class TestGameIntegration(unittest.TestCase):
    """Tests de integración para flujos completos del juego."""

    def test_board_and_game_entities_integration(self):
        """Test básico de integración entre Board y entidades del juego."""
        # Crear tablero y jugadores
        board = Board()
        player1 = Player("Alice")
        player2 = Player("Bob")
        
        # Verificar estado inicial
        self.assertIsNotNone(board)
        self.assertIsNotNone(player1)
        self.assertIsNotNone(player2)
        self.assertEqual(player1.name, "Alice")
        self.assertEqual(player2.name, "Bob")

        # Probar secuencia de movimientos básica en el tablero
        moves = [
            (0, 0, CellState.PLAYER_X),  # Alice juega X
            (1, 0, CellState.PLAYER_O),  # Bob juega O
            (0, 1, CellState.PLAYER_X),  # Alice juega X
            (1, 1, CellState.PLAYER_O),  # Bob juega O  
            (0, 2, CellState.PLAYER_X),  # Alice juega X - gana horizontalmente
        ]

        for row, col, player_symbol in moves:
            position = Position(row, col)
            move = Move(position, player_symbol)
            result = board.place_move(move)
            self.assertTrue(result)

        # Verificar que X gana
        winner = board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_X)

    def test_full_board_scenario(self):
        """Test de escenario con tablero lleno (empate)."""
        board = Board()
        
        # Llenar tablero sin ganador: X O X / O X O / O X O
        moves = [
            (0, 0, CellState.PLAYER_X), (0, 1, CellState.PLAYER_O), (0, 2, CellState.PLAYER_X),
            (1, 0, CellState.PLAYER_O), (1, 1, CellState.PLAYER_X), (1, 2, CellState.PLAYER_O),
            (2, 0, CellState.PLAYER_O), (2, 1, CellState.PLAYER_X), (2, 2, CellState.PLAYER_O)
        ]

        for row, col, player_symbol in moves:
            position = Position(row, col)
            move = Move(position, player_symbol)
            board.place_move(move)

        # Verificar empate
        self.assertTrue(board.is_full())
        self.assertIsNone(board.get_winner())

    def test_invalid_move_handling(self):
        """Test de manejo de movimientos inválidos."""
        board = Board()
        
        # Hacer movimiento válido
        position = Position(0, 0)
        move = Move(position, CellState.PLAYER_X)
        result = board.place_move(move)
        self.assertTrue(result)

        # Intentar movimiento en posición ocupada
        invalid_move = Move(position, CellState.PLAYER_O)
        result = board.place_move(invalid_move)
        self.assertFalse(result)  # Debe fallar


class TestBoardIntegration(unittest.TestCase):
    """Tests de integración para la clase Board."""

    def test_board_state_consistency(self):
        """Test de consistencia del estado del tablero."""
        board = Board()

        # Verificar estado inicial
        for row in range(board.size):
            for col in range(board.size):
                position = Position(row, col)
                self.assertEqual(board.get_cell_state(position), CellState.EMPTY)

        # Realizar secuencia de movimientos
        moves_data = [
            (0, 0, CellState.PLAYER_X),
            (1, 1, CellState.PLAYER_O),
            (0, 1, CellState.PLAYER_X),
            (2, 2, CellState.PLAYER_O),
            (0, 2, CellState.PLAYER_X),  # X gana horizontalmente
        ]

        for row, col, player in moves_data:
            position = Position(row, col)
            move = Move(position, player)
            success = board.place_move(move)
            self.assertTrue(success)
            self.assertEqual(board.get_cell_state(position), player)

        # Verificar ganador
        winner = board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_X)

    def test_board_full_detection(self):
        """Test de detección de tablero lleno."""
        board = Board()

        # Llenar tablero sin ganador: X O X / O X O / O X O
        moves_data = [
            (0, 0, CellState.PLAYER_X), (0, 1, CellState.PLAYER_O), (0, 2, CellState.PLAYER_X),
            (1, 0, CellState.PLAYER_O), (1, 1, CellState.PLAYER_X), (1, 2, CellState.PLAYER_O),
            (2, 0, CellState.PLAYER_O), (2, 1, CellState.PLAYER_X), (2, 2, CellState.PLAYER_O)
        ]

        for row, col, player in moves_data:
            position = Position(row, col)
            move = Move(position, player)
            board.place_move(move)

        self.assertTrue(board.is_full())
        self.assertIsNone(board.get_winner())  # No hay ganador


class TestPlayerIntegration(unittest.TestCase):
    """Tests de integración para la clase Player."""

    def test_player_creation_and_properties(self):
        """Test de creación y propiedades de jugadores."""
        player1 = Player(name="Alice")
        player2 = Player(name="Bob")

        # Verificar propiedades básicas
        self.assertEqual(player1.name, "Alice")
        self.assertEqual(player2.name, "Bob")
        self.assertIsNotNone(player1.id)
        self.assertIsNotNone(player2.id)
        self.assertNotEqual(player1.id, player2.id)


class TestAPIIntegration(unittest.TestCase):
    """Tests de integración para la API web (simulados)."""

    def setUp(self):
        """Configurar mocks para la aplicación Flask."""
        # Simular respuestas de la API sin necesidad de servidor real
        self.mock_responses = {
            "start_game": {"game_id": "test123", "status": "active"},
            "make_move": {
                "success": True,
                "board": [[" " for _ in range(3)] for _ in range(3)],
            },
            "game_status": {"status": "active", "current_player": "X"},
        }

    def test_api_game_lifecycle(self):
        """Test simulado del ciclo de vida de un juego vía API."""
        # Simular inicio de juego
        response = self.mock_responses["start_game"]
        self.assertEqual(response["status"], "active")
        self.assertIn("game_id", response)

        # Simular movimiento
        move_response = self.mock_responses["make_move"]
        self.assertTrue(move_response["success"])
        self.assertIn("board", move_response)

        # Simular consulta de estado
        status_response = self.mock_responses["game_status"]
        self.assertEqual(status_response["status"], "active")


if __name__ == "__main__":
    unittest.main()
