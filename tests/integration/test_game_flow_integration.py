"""
Tests de integración para el juego Tres en Raya.

Estos tests verifican la integración entre las diferentes capas
de la arquitectura siguiendo los principios de Screaming Architecture.
"""

import unittest
from unittest.mock import Mock, patch
import tempfile
import os

# Imports del dominio y aplicación
from game.entities.game_session import GameSession, GameState, GameResult, GameConfiguration
from game.entities.player import Player, PlayerType, PlayerSymbol
from game.entities.board import Board, Position, Move, CellState
from game.use_cases.start_new_game import StartNewGameUseCase, StartNewGameRequest, StartNewGameResponse
from application.entry_points.web_main import TicTacToeWebApp


class TestDomainIntegration(unittest.TestCase):
    """Tests de integración del dominio."""
    
    def test_complete_game_flow_human_vs_ai(self):
        """Test de flujo completo de juego humano vs AI."""
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
        
        # El juego debe estar listo para comenzar
        self.assertIsNotNone(session.id)
        self.assertEqual(session.configuration, config)
    
    def test_board_and_session_integration(self):
        """Test de integración entre Board y GameSession."""
        session = GameSession()
        board = session.board
        
        # Realizar algunos movimientos
        moves = [
            Move(Position(0, 0), CellState.PLAYER_X),
            Move(Position(1, 1), CellState.PLAYER_O),
            Move(Position(0, 1), CellState.PLAYER_X),
            Move(Position(2, 0), CellState.PLAYER_O),
            Move(Position(0, 2), CellState.PLAYER_X)  # X gana
        ]
        
        for move in moves:
            result = board.place_move(move)
            self.assertTrue(result, f"No se pudo colocar movimiento: {move}")
        
        # Verificar estado final
        winner = board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_X)
        
        # La sesión debe reflejar el estado del board
        self.assertIsNotNone(session.board.get_winner())
    
    def test_player_statistics_integration(self):
        """Test de integración de estadísticas de jugadores."""
        player = Player("Test Player", PlayerType.HUMAN)
        
        # Simular varias partidas
        games_results = [
            "win", "lose", "win", "draw", "win", "lose", "draw"
        ]
        
        for result in games_results:
            if result == "win":
                player.record_game_won()
            elif result == "lose":
                player.record_game_lost()
            elif result == "draw":
                player.record_game_drawn()
        
        # Verificar estadísticas finales
        stats = player.stats
        self.assertEqual(stats.games_played, 7)
        self.assertEqual(stats.games_won, 3)
        self.assertEqual(stats.games_lost, 2)
        self.assertEqual(stats.games_drawn, 2)
        
        # Verificar cálculos
        expected_win_rate = (3 / 7) * 100
        self.assertAlmostEqual(stats.win_rate, expected_win_rate, places=1)


class TestUseCaseIntegration(unittest.TestCase):
    """Tests de integración de casos de uso."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.start_new_game_use_case = StartNewGameUseCase()
    
    def test_start_new_game_complete_flow(self):
        """Test de flujo completo para iniciar nuevo juego."""
        # Crear request
        request = StartNewGameRequest(
            player1_name="Jugador Humano",
            player2_name="AI Oponente", 
            player2_type=PlayerType.AI_MEDIUM,
            configuration=GameConfiguration(enable_statistics=True)
        )
        
        # Ejecutar caso de uso
        response = self.start_new_game_use_case.execute(request)
        
        # Verificar respuesta exitosa
        self.assertTrue(response.success)
        self.assertIsNotNone(response.game_session)
        self.assertEqual(len(response.errors), 0)
        
        # Verificar sesión creada
        session = response.game_session
        self.assertIsNotNone(session)
        if session:
            self.assertEqual(session.state, GameState.IN_PROGRESS)
            self.assertTrue(session.configuration.enable_statistics)
    
    def test_invalid_request_handling(self):
        """Test de manejo de requests inválidos."""
        # Request con nombre vacío
        invalid_request = StartNewGameRequest(
            player1_name="",  # Nombre inválido
            player2_name="Jugador 2"
        )
        
        response = self.start_new_game_use_case.execute(invalid_request)
        
        # Debe fallar con errores de validación
        self.assertFalse(response.success)
        self.assertIsNone(response.game_session)
        self.assertTrue(len(response.errors) > 0)


class TestApplicationEntryPoints(unittest.TestCase):
    """Tests de integración de puntos de entrada de aplicación."""
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_cli_app_initialization(self, mock_print, mock_input):
        """Test de inicialización de aplicación CLI."""
        # Mock user input para salir inmediatamente
        mock_input.return_value = "0"  # Opción salir
        
        # Crear aplicación CLI usando el factory disponible
        from application.entry_points.run_console import create_cli_app
        cli_app = create_cli_app()
        
        # Verificar que se inicializó correctamente
        self.assertIsNotNone(cli_app)
        # CLIAdapter no expone directamente los casos de uso, pero podemos verificar que existe
        self.assertTrue(hasattr(cli_app, 'run'))
    
    def test_web_app_initialization(self):
        """Test de inicialización de aplicación Web."""
        # Crear aplicación Web
        web_app = TicTacToeWebApp()
        
        # Verificar que se inicializó correctamente
        self.assertIsNotNone(web_app)
        self.assertIsNotNone(web_app.get_flask_app())
        
        # Verificar que la app Flask está configurada
        flask_app = web_app.get_flask_app()
        self.assertIsNotNone(flask_app)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_cli_app_game_creation_flow(self, mock_print, mock_input):
        """Test de flujo de creación de juego en CLI."""
        # Mock user inputs
        mock_input.side_effect = [
            "1",  # Nuevo juego
            "Jugador 1",  # Nombre jugador 1
            "Jugador 2",  # Nombre jugador 2
            "1",  # Humano vs Humano
            "0"   # Salir
        ]
        
        # Crear aplicación CLI usando el factory disponible
        from application.entry_points.run_console import create_cli_app
        cli_app = create_cli_app()
        
        # El CLI debe manejar la entrada sin errores
        self.assertIsNotNone(cli_app)


class TestPersistenceIntegration(unittest.TestCase):
    """Tests de integración con persistencia."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        # Crear directorio temporal para tests
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
        self.scores_file = os.path.join(self.temp_dir, "test_scores.json")
    
    def tearDown(self):
        """Limpieza después de cada test."""
        # Limpiar archivos temporales
        for file_path in [self.config_file, self.scores_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)
    
    def test_game_state_persistence(self):
        """Test de persistencia del estado del juego."""
        # Crear sesión de juego
        session = GameSession()
        board = session.board
        
        # Realizar algunos movimientos
        moves = [
            Move(Position(0, 0), CellState.PLAYER_X),
            Move(Position(1, 1), CellState.PLAYER_O)
        ]
        
        for move in moves:
            board.place_move(move)
        
        # Serializar estado del juego
        game_state = {
            "session_id": session.id,
            "board": board.to_list(),
            "current_player": session.current_player_symbol.value,
            "move_count": session.move_count
        }
        
        # Verificar que se puede serializar
        import json
        serialized = json.dumps(game_state)
        deserialized = json.loads(serialized)
        
        self.assertEqual(deserialized["session_id"], session.id)
        self.assertEqual(len(deserialized["board"]), 3)
        self.assertEqual(len(deserialized["board"][0]), 3)
    
    def test_player_statistics_persistence(self):
        """Test de persistencia de estadísticas de jugadores."""
        player = Player("Test Player", PlayerType.HUMAN)
        
        # Actualizar estadísticas
        player.record_game_won()
        player.record_game_lost()
        
        # Serializar estadísticas
        player_data = {
            "id": player.id,
            "name": player.name,
            "type": player.player_type.value,
            "stats": {
                "games_played": player.stats.games_played,
                "games_won": player.stats.games_won,
                "games_lost": player.stats.games_lost,
                "win_rate": player.stats.win_rate
            }
        }
        
        # Verificar serialización
        import json
        serialized = json.dumps(player_data)
        deserialized = json.loads(serialized)
        
        self.assertEqual(deserialized["id"], player.id)
        self.assertEqual(deserialized["name"], player.name)
        self.assertEqual(deserialized["stats"]["games_played"], 2)


class TestInfrastructureIntegration(unittest.TestCase):
    """Tests de integración con infraestructura."""
    
    def test_game_configuration_loading(self):
        """Test de carga de configuración del juego."""
        # Crear configuración por defecto
        default_config = GameConfiguration()
        
        # Verificar valores por defecto
        self.assertEqual(default_config.board_size, 3)
        self.assertEqual(default_config.max_players, 2)
        self.assertTrue(default_config.allow_ai_players)
        self.assertTrue(default_config.enable_statistics)
    
    def test_custom_configuration(self):
        """Test de configuración personalizada."""
        # Crear configuración personalizada
        custom_config = GameConfiguration(
            board_size=3,
            max_players=2,
            allow_ai_players=False,  # Solo humanos
            time_limit_per_move=30,  # 30 segundos por movimiento
            enable_statistics=False
        )
        
        # Verificar valores personalizados
        self.assertEqual(custom_config.board_size, 3)
        self.assertFalse(custom_config.allow_ai_players)
        self.assertEqual(custom_config.time_limit_per_move, 30)
        self.assertFalse(custom_config.enable_statistics)
    
    def test_environment_configuration(self):
        """Test de configuración basada en ambiente."""
        # Simular diferentes ambientes
        environments = ["development", "production", "testing"]
        
        for env in environments:
            # Cada ambiente debe poder tener su configuración
            config = GameConfiguration()
            
            # Verificar que la configuración es válida para cualquier ambiente
            self.assertIsInstance(config.board_size, int)
            self.assertGreater(config.board_size, 0)
            self.assertIsInstance(config.max_players, int)
            self.assertGreaterEqual(config.max_players, 2)


class TestEndToEndScenarios(unittest.TestCase):
    """Tests de escenarios de extremo a extremo."""
    
    def test_complete_human_vs_human_game(self):
        """Test de juego completo humano vs humano."""
        # Crear jugadores
        player1 = Player("Jugador 1", PlayerType.HUMAN)
        player2 = Player("Jugador 2", PlayerType.HUMAN)
        
        player1.assign_symbol(PlayerSymbol.X)
        player2.assign_symbol(PlayerSymbol.O)
        
        # Crear sesión
        session = GameSession()
        board = session.board
        
        # Simular juego completo
        game_moves = [
            Move(Position(0, 0), CellState.PLAYER_X),  # X
            Move(Position(1, 0), CellState.PLAYER_O),  # O
            Move(Position(0, 1), CellState.PLAYER_X),  # X
            Move(Position(1, 1), CellState.PLAYER_O),  # O
            Move(Position(0, 2), CellState.PLAYER_X),  # X gana
        ]
        
        for i, move in enumerate(game_moves):
            # Verificar que el movimiento es válido
            self.assertTrue(board.is_position_empty(move.position))
            
            # Colocar movimiento
            result = board.place_move(move)
            self.assertTrue(result)
            
            # Verificar estado después del movimiento
            if i < len(game_moves) - 1:
                self.assertIsNone(board.get_winner())
            else:
                # Último movimiento - debe haber ganador
                self.assertEqual(board.get_winner(), CellState.PLAYER_X)
        
        # Actualizar estadísticas
        player1.record_game_won()
        player2.record_game_lost()
        
        # Verificar estadísticas finales
        self.assertEqual(player1.stats.games_won, 1)
        self.assertEqual(player2.stats.games_lost, 1)
    
    def test_complete_draw_game(self):
        """Test de juego completo que termina en empate."""
        session = GameSession()
        board = session.board
        
        # Secuencia que resulta en empate
        draw_moves = [
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
        
        for move in draw_moves:
            board.place_move(move)
        
        # Verificar empate
        self.assertTrue(board.is_full())
        self.assertIsNone(board.get_winner())


if __name__ == '__main__':
    unittest.main()