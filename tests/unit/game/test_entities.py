"""
Tests unitarios para las entidades del dominio del juego Tres en Raya.

Estos tests verifican el comportamiento de las entidades principales
del dominio siguiendo los principios de Screaming Architecture.
"""

import os
import sys
import unittest
from datetime import datetime

# Add project root to sys.path for imports
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    # Imports del dominio
    from game.entities.board import Board, Position, Move, CellState
    from game.entities.player import Player, PlayerType, PlayerSymbol, PlayerStats
    from game.entities.game_session import GameSession, GameState, GameResult, GameConfiguration
except ImportError as e:
    print(f"Error importing from game package: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise


class TestBoardEntity(unittest.TestCase):
    """Tests para la entidad Board (Tablero)."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.board = Board()
    
    def test_board_initialization(self):
        """Test de inicialización del tablero."""
        self.assertIsNotNone(self.board)
        self.assertFalse(self.board.is_full())
        self.assertIsNone(self.board.get_winner())
        
        # Verificar que todas las posiciones están vacías
        empty_positions = self.board.get_empty_positions()
        self.assertEqual(len(empty_positions), 9)  # 3x3 = 9 posiciones
    
    def test_position_creation(self):
        """Test de creación de posiciones."""
        pos = Position(0, 0)
        self.assertEqual(pos.row, 0)
        self.assertEqual(pos.col, 0)
        
        # Test de igualdad
        pos2 = Position(0, 0)
        self.assertEqual(pos, pos2)
        
        pos3 = Position(1, 1)
        self.assertNotEqual(pos, pos3)
    
    def test_move_creation(self):
        """Test de creación de movimientos."""
        position = Position(1, 1)
        move = Move(position=position, player=CellState.PLAYER_X)
        
        self.assertEqual(move.position, position)
        self.assertEqual(move.player, CellState.PLAYER_X)
    
    def test_place_move(self):
        """Test de colocación de movimientos."""
        position = Position(0, 0)
        move = Move(position=position, player=CellState.PLAYER_X)
        
        # Colocar movimiento
        result = self.board.place_move(move)
        self.assertTrue(result)
        
        # Verificar que la posición ya no está vacía
        self.assertFalse(self.board.is_position_empty(position))
        
        # Verificar que el movimiento se registró correctamente
        board_state = self.board.to_list()
        self.assertEqual(board_state[0][0], 'X')
    
    def test_invalid_move_placement(self):
        """Test de colocación de movimientos inválidos."""
        position = Position(0, 0)
        move1 = Move(position=position, player=CellState.PLAYER_X)
        move2 = Move(position=position, player=CellState.PLAYER_O)
        
        # Colocar primer movimiento
        result1 = self.board.place_move(move1)
        self.assertTrue(result1)
        
        # Intentar colocar segundo movimiento en la misma posición
        result2 = self.board.place_move(move2)
        self.assertFalse(result2)
    
    def test_winning_condition_horizontal(self):
        """Test de condición de victoria horizontal."""
        # Crear línea horizontal ganadora
        moves = [
            Move(Position(0, 0), CellState.PLAYER_X),
            Move(Position(0, 1), CellState.PLAYER_X),
            Move(Position(0, 2), CellState.PLAYER_X)
        ]
        
        for move in moves:
            self.board.place_move(move)
        
        winner = self.board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_X)
    
    def test_winning_condition_vertical(self):
        """Test de condición de victoria vertical."""
        # Crear línea vertical ganadora
        moves = [
            Move(Position(0, 0), CellState.PLAYER_O),
            Move(Position(1, 0), CellState.PLAYER_O),
            Move(Position(2, 0), CellState.PLAYER_O)
        ]
        
        for move in moves:
            self.board.place_move(move)
        
        winner = self.board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_O)
    
    def test_winning_condition_diagonal(self):
        """Test de condición de victoria diagonal."""
        # Crear línea diagonal ganadora
        moves = [
            Move(Position(0, 0), CellState.PLAYER_X),
            Move(Position(1, 1), CellState.PLAYER_X),
            Move(Position(2, 2), CellState.PLAYER_X)
        ]
        
        for move in moves:
            self.board.place_move(move)
        
        winner = self.board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_X)
    
    def test_board_full_condition(self):
        """Test de condición de tablero lleno."""
        # Llenar el tablero sin crear ganador
        positions = [
            (Position(0, 0), CellState.PLAYER_X),  # X
            (Position(0, 1), CellState.PLAYER_O),  # O
            (Position(0, 2), CellState.PLAYER_X),  # X
            (Position(1, 0), CellState.PLAYER_O),  # O
            (Position(1, 1), CellState.PLAYER_O),  # O
            (Position(1, 2), CellState.PLAYER_X),  # X
            (Position(2, 0), CellState.PLAYER_X),  # X
            (Position(2, 1), CellState.PLAYER_X),  # X
            (Position(2, 2), CellState.PLAYER_O)   # O
        ]
        
        for position, player in positions:
            move = Move(position=position, player=player)
            self.board.place_move(move)
        
        self.assertTrue(self.board.is_full())
        self.assertIsNone(self.board.get_winner())  # Empate
    
    def test_reset_board(self):
        """Test de reinicio del tablero."""
        # Colocar algunos movimientos
        position = Position(1, 1)
        move = Move(position=position, player=CellState.PLAYER_X)
        self.board.place_move(move)
        
        # Verificar que el movimiento se colocó
        self.assertFalse(self.board.is_position_empty(position))
        
        # Reiniciar
        self.board.reset()
        
        # Verificar que el tablero está limpio
        self.assertTrue(self.board.is_position_empty(position))
        self.assertEqual(len(self.board.get_empty_positions()), 9)
        self.assertIsNone(self.board.get_winner())


class TestPlayerEntity(unittest.TestCase):
    """Tests para la entidad Player (Jugador)."""
    
    def test_player_creation(self):
        """Test de creación de jugador."""
        player = Player("Juan", PlayerType.HUMAN)
        
        self.assertEqual(player.name, "Juan")
        self.assertEqual(player.player_type, PlayerType.HUMAN)
        self.assertIsNotNone(player.id)
        self.assertIsNone(player.symbol)
        self.assertTrue(player.is_active)
        self.assertIsInstance(player.created_at, datetime)
    
    def test_player_symbol_assignment(self):
        """Test de asignación de símbolo al jugador."""
        player = Player("Ana", PlayerType.HUMAN)
        
        # Asignar símbolo
        player.assign_symbol(PlayerSymbol.X)
        self.assertEqual(player.symbol, PlayerSymbol.X)
        
        # Intentar cambiar símbolo debe fallar
        with self.assertRaises(ValueError):
            player.assign_symbol(PlayerSymbol.O)
    
    def test_player_name_validation(self):
        """Test de validación del nombre del jugador."""
        # Nombre válido
        player = Player("Jugador 1", PlayerType.HUMAN)
        self.assertEqual(player.name, "Jugador 1")
        
        # Nombre vacío debe fallar
        with self.assertRaises(ValueError):
            Player("", PlayerType.HUMAN)
        
        # Nombre solo espacios debe fallar
        with self.assertRaises(ValueError):
            Player("   ", PlayerType.HUMAN)
    
    def test_player_statistics(self):
        """Test de estadísticas del jugador."""
        player = Player("TestPlayer", PlayerType.HUMAN)
        
        # Estadísticas iniciales
        stats = player.stats
        self.assertEqual(stats.games_played, 0)
        self.assertEqual(stats.games_won, 0)
        self.assertEqual(stats.games_lost, 0)
        self.assertEqual(stats.games_drawn, 0)
        self.assertEqual(stats.win_rate, 0.0)
        
        # Registrar victoria
        player.record_game_won()
        stats = player.stats
        self.assertEqual(stats.games_played, 1)
        self.assertEqual(stats.games_won, 1)
        self.assertEqual(stats.win_rate, 100.0)
        
        # Registrar derrota
        player.record_game_lost()
        stats = player.stats
        self.assertEqual(stats.games_played, 2)
        self.assertEqual(stats.games_lost, 1)
        self.assertEqual(stats.win_rate, 50.0)
    
    def test_player_equality(self):
        """Test de igualdad entre jugadores."""
        player1 = Player("Juan", PlayerType.HUMAN, "test-id-1")
        player2 = Player("Ana", PlayerType.AI_EASY, "test-id-1")  # Mismo ID
        player3 = Player("Juan", PlayerType.HUMAN, "test-id-2")   # Diferente ID
        
        # Los jugadores con mismo ID son iguales
        self.assertEqual(player1, player2)
        
        # Los jugadores con diferente ID no son iguales
        self.assertNotEqual(player1, player3)
    
    def test_player_types(self):
        """Test de tipos de jugador."""
        human_player = Player("Human", PlayerType.HUMAN)
        ai_easy = Player("AI Easy", PlayerType.AI_EASY)
        ai_medium = Player("AI Medium", PlayerType.AI_MEDIUM)
        ai_hard = Player("AI Hard", PlayerType.AI_HARD)
        
        self.assertTrue(human_player.is_human)
        self.assertFalse(human_player.is_ai)
        
        self.assertFalse(ai_easy.is_human)
        self.assertTrue(ai_easy.is_ai)
        
        self.assertTrue(ai_medium.is_ai)
        self.assertTrue(ai_hard.is_ai)


class TestPlayerStats(unittest.TestCase):
    """Tests para PlayerStats (Estadísticas del Jugador)."""
    
    def test_stats_initialization(self):
        """Test de inicialización de estadísticas."""
        stats = PlayerStats()
        
        self.assertEqual(stats.games_played, 0)
        self.assertEqual(stats.games_won, 0)
        self.assertEqual(stats.games_lost, 0)
        self.assertEqual(stats.games_drawn, 0)
    
    def test_win_rate_calculation(self):
        """Test de cálculo de tasa de victoria."""
        # Sin juegos
        stats = PlayerStats()
        self.assertEqual(stats.win_rate, 0.0)
        
        # Con juegos
        stats = PlayerStats(games_played=10, games_won=7, games_lost=2, games_drawn=1)
        self.assertEqual(stats.win_rate, 70.0)
        
        # 100% victorias
        stats = PlayerStats(games_played=5, games_won=5, games_lost=0, games_drawn=0)
        self.assertEqual(stats.win_rate, 100.0)
    
    def test_loss_rate_calculation(self):
        """Test de cálculo de tasa de derrota."""
        stats = PlayerStats(games_played=10, games_won=6, games_lost=3, games_drawn=1)
        self.assertEqual(stats.loss_rate, 30.0)
    
    def test_draw_rate_calculation(self):
        """Test de cálculo de tasa de empate."""
        stats = PlayerStats(games_played=10, games_won=5, games_lost=3, games_drawn=2)
        self.assertEqual(stats.draw_rate, 20.0)


class TestGameSession(unittest.TestCase):
    """Tests para la entidad GameSession (Sesión de Juego)."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.player1 = Player("Jugador 1", PlayerType.HUMAN)
        self.player2 = Player("Jugador 2", PlayerType.HUMAN)
        self.config = GameConfiguration()
    
    def test_game_session_creation(self):
        """Test de creación de sesión de juego."""
        session = GameSession(configuration=self.config)
        
        self.assertIsNotNone(session.id)
        self.assertEqual(session.state, GameState.WAITING_FOR_PLAYERS)
        self.assertIsNone(session.result)
        self.assertIsInstance(session.created_at, datetime)
        self.assertEqual(session.current_player_symbol, PlayerSymbol.X)
        self.assertEqual(len(session.players), 0)  # Sin jugadores inicialmente
    
    def test_game_configuration(self):
        """Test de configuración del juego."""
        config = GameConfiguration(
            board_size=3,
            max_players=2,
            allow_ai_players=True,
            time_limit_per_move=30
        )
        
        session = GameSession(configuration=config)
        
        self.assertEqual(session.configuration.board_size, 3)
        self.assertEqual(session.configuration.max_players, 2)
        self.assertTrue(session.configuration.allow_ai_players)
        self.assertEqual(session.configuration.time_limit_per_move, 30)
    
    def test_player_properties(self):
        """Test de propiedades de jugadores."""
        session = GameSession()
        
        # Inicialmente sin jugadores
        self.assertIsNone(session.player_x)
        self.assertIsNone(session.player_o)
        self.assertIsNone(session.current_player)
        
        # El símbolo actual debe ser X
        self.assertEqual(session.current_player_symbol, PlayerSymbol.X)


if __name__ == '__main__':
    unittest.main()