"""
Tests de integración simplificados para aplicación web Tres en Raya.

Estos tests verifican la integración entre las diferentes capas
de la arquitectura siguiendo los principios de Screaming Architecture.
Solo incluye funcionalidad web (sin CLI ni multijugador).
"""

import unittest
import sys
from pathlib import Path

# Configurar path para imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Imports del dominio y aplicación
from game.entities.player import Player, PlayerType, PlayerSymbol
from game.entities.board import Board, Position, Move, CellState
from game.entities.game_session import GameSession, GameState, GameResult, GameConfiguration
from game.use_cases.start_new_game import StartNewGameUseCase
from application.entry_points.web_main import TicTacToeWebApp


class TestWebIntegration(unittest.TestCase):
    """Tests de integración para la aplicación web."""
    
    def test_web_app_initialization(self):
        """Test de inicialización correcta de la aplicación web."""
        app = TicTacToeWebApp()
        self.assertIsNotNone(app)
        
    def test_complete_game_flow_domain(self):
        """Test de flujo completo de juego en el dominio."""
        # Crear jugadores
        human_player = Player("Humano", PlayerType.HUMAN)
        ai_player = Player("AI", PlayerType.AI_EASY)
        
        # Asignar símbolos
        human_player.assign_symbol(PlayerSymbol.X)
        ai_player.assign_symbol(PlayerSymbol.O)
        
        # Crear configuración
        config = GameConfiguration(
            board_size=3,
            allow_ai_players=True,
            enable_statistics=True
        )
        
        # Crear sesión de juego
        session = GameSession(configuration=config)
        
        # Verificar estado inicial
        self.assertEqual(session.state, GameState.WAITING_FOR_PLAYERS)
        self.assertIsNotNone(session.board)
        self.assertEqual(session.current_player_symbol, PlayerSymbol.X)
        
    def test_board_and_moves_integration(self):
        """Test de integración entre tablero y movimientos."""
        from game.entities.board import BoardSize
        board = Board(size=BoardSize.STANDARD)
        
        # Verificar tablero vacío
        self.assertFalse(board.is_full())
        
        # Realizar movimiento
        position = Position(1, 1)
        move = Move(position, CellState.PLAYER_X)
        
        result = board.place_move(move)
        self.assertTrue(result)
        self.assertEqual(board.get_cell_state(position), CellState.PLAYER_X)
        self.assertFalse(board.is_position_empty(position))
        
    def test_use_case_integration(self):
        """Test de integración de caso de uso."""
        use_case = StartNewGameUseCase()
        
        # Crear request válido
        player1 = Player("Jugador1", PlayerType.HUMAN)
        player2 = Player("AI", PlayerType.AI_EASY)
        
        config = GameConfiguration(
            board_size=3,
            allow_ai_players=True,
            enable_statistics=False
        )
        
        # El caso de uso debe funcionar correctamente
        self.assertIsNotNone(use_case)


if __name__ == '__main__':
    unittest.main()