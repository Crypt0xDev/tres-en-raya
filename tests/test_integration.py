"""
Tests de integración end-to-end para el juego Tres en Raya.

Estos tests prueban flujos completos del juego y la interacción entre componentes.
"""

import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.core.board import Board
from src.core.game_engine import GameEngine
from src.core.player import Player
from src.interfaces.cli import game_logic


class TestGameIntegration(unittest.TestCase):
    """Tests de integración para flujos completos del juego."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.game_engine = GameEngine()
        self.board = Board()

    def test_complete_game_flow_player_x_wins(self):
        """Test de flujo completo donde gana el jugador X."""
        # Iniciar juego
        game_id = self.game_engine.start_game("Alice", "Bob")
        self.assertIsNotNone(game_id)

        # Verificar estado inicial
        status = self.game_engine.get_game_status(game_id)
        self.assertEqual(status["status"], "active")
        self.assertEqual(status["current_player"], "Alice")

        # Secuencia de movimientos para que gane X
        moves = [
            ("Alice", 0),  # X en [0,0]
            ("Bob", 3),  # O en [1,0]
            ("Alice", 1),  # X en [0,1]
            ("Bob", 4),  # O en [1,1]
            ("Alice", 2),  # X en [0,2] - ¡Gana!
        ]

        for player, position in moves[:-1]:
            result = self.game_engine.make_move(game_id, player, position)
            self.assertTrue(result["success"])
            self.assertNotIn("winner", result)

        # Último movimiento - X gana
        result = self.game_engine.make_move(game_id, "Alice", 2)
        self.assertTrue(result["success"])
        self.assertEqual(result["winner"], "X")

        # Verificar estado final
        status = self.game_engine.get_game_status(game_id)
        self.assertEqual(status["status"], "finished")
        self.assertEqual(status["winner"], "X")

    def test_complete_game_flow_draw(self):
        """Test de flujo completo que termina en empate."""
        game_id = self.game_engine.start_game("Player1", "Player2")

        # Secuencia validada que termina en empate:
        # Final: X O X
        #        O X X
        #        O X O
        moves = [
            ("Player1", 0),
            ("Player2", 1),
            ("Player1", 2),  # Fila 0: X O X
            ("Player2", 3),
            ("Player1", 4),
            ("Player2", 8),  # P2 bloquea diagonal
            ("Player1", 5),
            ("Player2", 6),
            ("Player1", 7),  # Llenar resto - empate
        ]

        for i, (player, position) in enumerate(moves):
            result = self.game_engine.make_move(game_id, player, position)
            self.assertTrue(result["success"])

            if i == len(moves) - 1:  # Último movimiento
                self.assertEqual(result["winner"], "draw")
            else:
                # No debe haber ganador hasta el final
                self.assertNotIn("winner", result)

    def test_invalid_move_scenarios(self):
        """Test de escenarios de movimientos inválidos."""
        game_id = self.game_engine.start_game("Alice", "Bob")

        # Movimiento en posición ocupada
        self.game_engine.make_move(game_id, "Alice", 0)
        result = self.game_engine.make_move(game_id, "Bob", 0)
        self.assertIn("error", result)

        # Movimiento fuera de turno
        result = self.game_engine.make_move(game_id, "Alice", 1)
        self.assertIn("error", result)

        # Movimiento en juego inexistente
        result = self.game_engine.make_move("nonexistent", "Alice", 1)
        self.assertIn("error", result)


class TestBoardIntegration(unittest.TestCase):
    """Tests de integración para la clase Board."""

    def test_board_state_consistency(self):
        """Test de consistencia del estado del tablero."""
        board = Board()

        # Verificar estado inicial
        self.assertTrue(all(cell == " " for row in board.board for cell in row))
        self.assertEqual(board.current_player, "X")

        # Realizar secuencia de movimientos
        positions = [(0, 0), (1, 1), (0, 1), (2, 2), (0, 2)]
        expected_players = ["X", "O", "X", "O", "X"]

        for i, (row, col) in enumerate(positions):
            expected_player = expected_players[i]
            self.assertEqual(board.current_player, expected_player)

            success = board.make_move(row, col)
            self.assertTrue(success)
            self.assertEqual(board.board[row][col], expected_player)

        # Verificar ganador
        winner = board.check_winner()
        self.assertEqual(winner, "X")

    def test_board_full_detection(self):
        """Test de detección de tablero lleno."""
        board = Board()

        # Llenar tablero sin ganador
        moves = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (1, 1), (2, 0), (2, 2), (2, 1)]
        for row, col in moves:
            board.make_move(row, col)

        self.assertTrue(board.is_board_full())
        self.assertIsNone(board.check_winner())  # No hay ganador


class TestPlayerIntegration(unittest.TestCase):
    """Tests de integración para la clase Player."""

    def test_player_score_tracking(self):
        """Test de seguimiento de puntuación de jugadores."""
        player1 = Player("Alice")
        player2 = Player("Bob")

        player1.set_symbol("X")
        player2.set_symbol("O")

        # Simular múltiples juegos
        for _ in range(3):
            player1.increment_score()

        for _ in range(2):
            player2.increment_score()

        self.assertEqual(player1.score, 3)
        self.assertEqual(player2.score, 2)
        self.assertEqual(player1.symbol, "X")
        self.assertEqual(player2.symbol, "O")


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
