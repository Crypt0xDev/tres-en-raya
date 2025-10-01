"""
Tests unitarios para los casos de uso del dominio del juego Tres en Raya.

Estos tests verifican el comportamiento de los casos de uso principales
del dominio siguiendo los principios de Screaming Architecture.
"""

import unittest

# Imports del dominio  
from game.entities import (
    Board, Position, Move, CellState,
    Player, PlayerType, PlayerSymbol,
    GameSession, GameState, GameResult, GameConfiguration
)
from game.use_cases.start_new_game import StartNewGameUseCase, StartNewGameRequest


class TestStartNewGameUseCase(unittest.TestCase):
    """Tests para el caso de uso StartNewGame."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.use_case = StartNewGameUseCase()
    
    def test_start_new_game_request_creation(self):
        """Test de creación de request para nuevo juego."""
        request = StartNewGameRequest(
            player1_name="Jugador 1",
            player2_name="Jugador 2",
            player2_type=PlayerType.HUMAN
        )
        
        self.assertEqual(request.player1_name, "Jugador 1")
        self.assertEqual(request.player2_name, "Jugador 2")
        self.assertEqual(request.player2_type, PlayerType.HUMAN)
        self.assertIsNone(request.configuration)
    
    def test_start_new_game_with_ai_player(self):
        """Test de inicio de juego con jugador AI."""
        request = StartNewGameRequest(
            player1_name="Humano",
            player2_name="AI Fácil",
            player2_type=PlayerType.AI_EASY
        )
        
        response = self.use_case.execute(request)
        
        # Verificar que la respuesta es exitosa
        self.assertTrue(response.success)
        self.assertIsNotNone(response.game_session)
        self.assertEqual(len(response.errors), 0)
    
    def test_start_new_game_with_custom_config(self):
        """Test de inicio de juego con configuración personalizada."""
        config = GameConfiguration(
            board_size=3,
            allow_ai_players=True,
            time_limit_per_move=60,
            enable_statistics=True
        )
        
        request = StartNewGameRequest(
            player1_name="Jugador 1",
            player2_name="Jugador 2",
            configuration=config
        )
        
        response = self.use_case.execute(request)
        
        self.assertTrue(response.success)
        self.assertIsNotNone(response.game_session)
        self.assertEqual(response.game_session.configuration.board_size, 3)
        self.assertTrue(response.game_session.configuration.allow_ai_players)
    
    def test_start_game_invalid_player_names(self):
        """Test de validación de nombres de jugadores inválidos."""
        # Nombre vacío
        request = StartNewGameRequest(
            player1_name="",
            player2_name="Jugador 2"
        )
        
        response = self.use_case.execute(request)
        
        self.assertFalse(response.success)
        self.assertTrue(len(response.errors) > 0)
        self.assertIn("player1_name", str(response.errors))


class TestBoardGameLogic(unittest.TestCase):
    """Tests de lógica de juego usando el tablero directamente."""
    
    def test_complete_game_x_wins(self):
        """Test de juego completo donde gana X."""
        board = Board()
        
        # Secuencia de movimientos donde X gana
        moves = [
            Move(Position(0, 0), CellState.PLAYER_X),  # X
            Move(Position(1, 0), CellState.PLAYER_O),  # O
            Move(Position(0, 1), CellState.PLAYER_X),  # X
            Move(Position(1, 1), CellState.PLAYER_O),  # O
            Move(Position(0, 2), CellState.PLAYER_X),  # X gana (fila superior)
        ]
        
        # Ejecutar movimientos
        for move in moves[:-1]:
            board.place_move(move)
            self.assertIsNone(board.get_winner())  # Aún no hay ganador
        
        # Último movimiento - X gana
        board.place_move(moves[-1])
        self.assertEqual(board.get_winner(), CellState.PLAYER_X)
    
    def test_complete_game_draw(self):
        """Test de juego completo que termina en empate."""
        board = Board()
        
        # Secuencia que lleva a empate
        moves = [
            Move(Position(0, 0), CellState.PLAYER_X),  # X
            Move(Position(0, 1), CellState.PLAYER_O),  # O  
            Move(Position(0, 2), CellState.PLAYER_X),  # X
            Move(Position(1, 0), CellState.PLAYER_O),  # O
            Move(Position(1, 1), CellState.PLAYER_O),  # O
            Move(Position(1, 2), CellState.PLAYER_X),  # X
            Move(Position(2, 0), CellState.PLAYER_X),  # X
            Move(Position(2, 1), CellState.PLAYER_X),  # X
            Move(Position(2, 2), CellState.PLAYER_O),  # O - Empate
        ]
        
        for move in moves:
            board.place_move(move)
        
        # Verificar empate
        self.assertTrue(board.is_full())
        self.assertIsNone(board.get_winner())


class TestGameSessionWorkflow(unittest.TestCase):
    """Tests del flujo de trabajo de GameSession."""
    
    def test_game_session_lifecycle(self):
        """Test del ciclo de vida completo de una sesión de juego."""
        # Crear configuración
        config = GameConfiguration(enable_statistics=True)
        
        # Crear sesión
        session = GameSession(configuration=config)
        
        # Verificar estado inicial
        self.assertEqual(session.state, GameState.WAITING_FOR_PLAYERS)
        self.assertIsNone(session.result)
        self.assertEqual(session.current_player_symbol, PlayerSymbol.X)
        
        # Verificar propiedades
        self.assertIsNotNone(session.id)
        self.assertEqual(session.configuration, config)
        self.assertIsNotNone(session.board)
        self.assertEqual(session.move_count, 0)


class TestPlayerManagement(unittest.TestCase):
    """Tests de gestión de jugadores."""
    
    def test_create_human_player(self):
        """Test de creación de jugador humano."""
        player = Player("Juan", PlayerType.HUMAN)
        
        self.assertEqual(player.name, "Juan")
        self.assertEqual(player.player_type, PlayerType.HUMAN)
        self.assertTrue(player.is_human)
        self.assertFalse(player.is_ai)
        self.assertTrue(player.is_active)
        
        # Verificar estadísticas iniciales
        stats = player.stats
        self.assertEqual(stats.games_played, 0)
        self.assertEqual(stats.win_rate, 0.0)
    
    def test_create_ai_players(self):
        """Test de creación de jugadores AI."""
        ai_easy = Player("AI Fácil", PlayerType.AI_EASY)
        ai_medium = Player("AI Medio", PlayerType.AI_MEDIUM)
        ai_hard = Player("AI Difícil", PlayerType.AI_HARD)
        
        # Verificar que todos son AI
        for ai_player in [ai_easy, ai_medium, ai_hard]:
            self.assertFalse(ai_player.is_human)
            self.assertTrue(ai_player.is_ai)
    
    def test_player_symbol_assignment(self):
        """Test de asignación de símbolos a jugadores."""
        player1 = Player("Jugador 1", PlayerType.HUMAN)
        player2 = Player("Jugador 2", PlayerType.HUMAN)
        
        # Asignar símbolos
        player1.assign_symbol(PlayerSymbol.X)
        player2.assign_symbol(PlayerSymbol.O)
        
        self.assertEqual(player1.symbol, PlayerSymbol.X)
        self.assertEqual(player2.symbol, PlayerSymbol.O)
        
        # Verificar que no se puede cambiar símbolo una vez asignado
        with self.assertRaises(ValueError):
            player1.assign_symbol(PlayerSymbol.O)
    
    def test_player_statistics_update(self):
        """Test de actualización de estadísticas de jugador."""
        player = Player("Test Player", PlayerType.HUMAN)
        
        # Registrar algunas partidas
        player.record_game_won()
        player.record_game_won()
        player.record_game_lost()
        player.record_game_drawn()
        
        stats = player.stats
        self.assertEqual(stats.games_played, 4)
        self.assertEqual(stats.games_won, 2)
        self.assertEqual(stats.games_lost, 1)
        self.assertEqual(stats.games_drawn, 1)
        self.assertEqual(stats.win_rate, 50.0)  # 2/4 = 0.5 = 50%


if __name__ == '__main__':
    unittest.main()