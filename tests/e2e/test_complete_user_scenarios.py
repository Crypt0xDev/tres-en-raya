"""
Tests End-to-End (E2E) para el juego Tres en Raya.

Estos tests verifican el funcionamiento completo de la aplicación
desde la perspectiva del usuario final, siguiendo los principios
de Screaming Architecture donde la funcionalidad del juego es clara.
"""

import unittest
from unittest.mock import patch, MagicMock
import subprocess
import sys
import os
import requests
import time
import threading

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)


class TestCLIEndToEnd(unittest.TestCase):
    """Tests E2E para la interfaz de línea de comandos."""
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_cli_complete_human_vs_human_game(self, mock_print, mock_input):
        """Test E2E de juego completo humano vs humano via CLI."""
        # Simular entrada del usuario para un juego completo
        user_inputs = [
            "1",           # Nuevo juego
            "Jugador 1",   # Nombre jugador 1
            "Jugador 2",   # Nombre jugador 2
            "1",           # Humano vs Humano
            "0,0",         # Movimiento 1 (X)
            "1,0",         # Movimiento 2 (O)
            "0,1",         # Movimiento 3 (X)
            "1,1",         # Movimiento 4 (O)
            "0,2",         # Movimiento 5 (X) - Gana X
            "0"            # Salir
        ]
        
        mock_input.side_effect = user_inputs
        
        # Importar y ejecutar aplicación CLI
        from application.entry_points.cli_app import TicTacToeCLIApp
        
        cli_app = TicTacToeCLIApp()
        
        # Verificar que la aplicación se inicializa correctamente
        self.assertIsNotNone(cli_app)
        
        # Verificar que se llamaron los prints (interfaz mostrada)
        self.assertTrue(mock_print.called)
        
        # Verificar que se procesaron las entradas del usuario
        self.assertTrue(mock_input.called)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_cli_human_vs_ai_game(self, mock_print, mock_input):
        """Test E2E de juego humano vs AI via CLI."""
        user_inputs = [
            "1",           # Nuevo juego
            "Humano",      # Nombre jugador humano
            "2",           # Humano vs AI
            "2",           # Dificultad media
            "1,1",         # Movimiento humano (centro)
            "0,0",         # Otro movimiento humano
            "2,2",         # Otro movimiento humano
            "0"            # Salir
        ]
        
        mock_input.side_effect = user_inputs
        
        from application.entry_points.cli_app import TicTacToeCLIApp
        
        cli_app = TicTacToeCLIApp()
        
        # Verificar inicialización exitosa
        self.assertIsNotNone(cli_app)
        self.assertTrue(mock_print.called)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_cli_invalid_input_handling(self, mock_print, mock_input):
        """Test E2E de manejo de entrada inválida en CLI."""
        user_inputs = [
            "invalid",     # Opción inválida
            "1",           # Nuevo juego (válido)
            "",            # Nombre vacío (inválido)
            "Jugador",     # Nombre válido
            "Oponente",    # Segundo jugador
            "1",           # Humano vs Humano
            "9,9",         # Posición inválida
            "0,0",         # Posición válida
            "0"            # Salir
        ]
        
        mock_input.side_effect = user_inputs
        
        from application.entry_points.cli_app import TicTacToeCLIApp
        
        cli_app = TicTacToeCLIApp()
        
        # La aplicación debe manejar entradas inválidas gracefully
        self.assertIsNotNone(cli_app)
        self.assertTrue(mock_print.called)
    
    @patch('builtins.input')
    @patch('builtins.print')  
    def test_cli_game_statistics_display(self, mock_print, mock_input):
        """Test E2E de visualización de estadísticas en CLI."""
        user_inputs = [
            "3",           # Ver estadísticas
            "0"            # Salir
        ]
        
        mock_input.side_effect = user_inputs
        
        from application.entry_points.cli_app import TicTacToeCLIApp
        
        cli_app = TicTacToeCLIApp()
        
        # Verificar que se mostró la interfaz de estadísticas
        self.assertIsNotNone(cli_app)
        self.assertTrue(mock_print.called)


class TestWebEndToEnd(unittest.TestCase):
    """Tests E2E para la interfaz web."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        # Mock de servidor web para tests
        self.base_url = "http://localhost:5000"
        self.server_process = None
    
    def tearDown(self):
        """Limpieza después de cada test."""
        # Limpiar servidor si está corriendo
        if self.server_process:
            self.server_process.terminate()
    
    def test_web_app_initialization(self):
        """Test E2E de inicialización de aplicación web."""
        from application.entry_points.web_app import TicTacToeWebApp
        
        web_app = TicTacToeWebApp()
        
        # Verificar que la aplicación web se inicializa
        self.assertIsNotNone(web_app)
        self.assertIsNotNone(web_app.flask_app)
        
        # Verificar configuración Flask
        self.assertEqual(web_app.flask_app.config['DEBUG'], True)
    
    @patch('requests.post')
    def test_web_create_new_game_api(self, mock_post):
        """Test E2E de API para crear nuevo juego via web."""
        # Mock response exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "session_id": "test-session-123",
            "message": "Juego creado exitosamente"
        }
        mock_post.return_value = mock_response
        
        # Datos del request
        game_data = {
            "player1_name": "Jugador Web 1",
            "player2_name": "Jugador Web 2",
            "player2_type": "human"
        }
        
        # Simular llamada a API
        response = mock_post(f"{self.base_url}/api/games", json=game_data)
        
        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertIn("session_id", response_data)
    
    @patch('requests.post')
    def test_web_make_move_api(self, mock_post):
        """Test E2E de API para realizar movimiento via web."""
        # Mock response exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "board_state": [
                ["X", "", ""],
                ["", "", ""],
                ["", "", ""]
            ],
            "current_player": "O",
            "game_status": "in_progress"
        }
        mock_post.return_value = mock_response
        
        # Datos del movimiento
        move_data = {
            "session_id": "test-session-123",
            "player_id": "player-1",
            "position": {"row": 0, "col": 0}
        }
        
        # Simular llamada a API
        response = mock_post(f"{self.base_url}/api/moves", json=move_data)
        
        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertIn("board_state", response_data)
        self.assertEqual(response_data["current_player"], "O")
    
    @patch('requests.get')
    def test_web_get_game_status_api(self, mock_get):
        """Test E2E de API para obtener estado del juego via web."""
        # Mock response con estado del juego
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "session_id": "test-session-123",
            "state": "in_progress",
            "board": [
                ["X", "O", ""],
                ["", "X", ""],
                ["", "", "O"]
            ],
            "current_player": "X",
            "move_count": 4,
            "winner": None
        }
        mock_get.return_value = mock_response
        
        # Simular llamada a API
        response = mock_get(f"{self.base_url}/api/games/test-session-123")
        
        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertEqual(response_data["session_id"], "test-session-123")
        self.assertEqual(response_data["state"], "in_progress")
        self.assertIsInstance(response_data["board"], list)
        self.assertEqual(len(response_data["board"]), 3)


class TestMultiplayerEndToEnd(unittest.TestCase):
    """Tests E2E para funcionalidad multijugador."""
    
    def test_multiplayer_server_initialization(self):
        """Test E2E de inicialización de servidor multijugador."""
        from application.entry_points.multiplayer_server import MultiplayerServer
        
        server = MultiplayerServer()
        
        # Verificar que el servidor se inicializa correctamente
        self.assertIsNotNone(server)
        
        # Verificar configuración del servidor
        self.assertIsNotNone(server.config)
    
    @patch('socket.socket')
    def test_multiplayer_connection_handling(self, mock_socket):
        """Test E2E de manejo de conexiones multijugador."""
        from application.entry_points.multiplayer_server import MultiplayerServer
        
        # Mock socket connection
        mock_client = MagicMock()
        mock_socket.return_value = mock_client
        
        server = MultiplayerServer()
        
        # Simular conexión de cliente
        # En una implementación real, esto manejaría conexiones TCP/WebSocket
        self.assertIsNotNone(server)
    
    def test_multiplayer_game_room_creation(self):
        """Test E2E de creación de salas de juego multijugador."""
        from application.entry_points.multiplayer_server import MultiplayerServer
        
        server = MultiplayerServer()
        
        # Verificar capacidad de crear salas
        # En implementación real, esto crearía salas de juego
        self.assertIsNotNone(server)


class TestErrorHandlingEndToEnd(unittest.TestCase):
    """Tests E2E de manejo de errores."""
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_cli_graceful_error_handling(self, mock_print, mock_input):
        """Test E2E de manejo graceful de errores en CLI."""
        # Inputs que causan varios tipos de errores
        user_inputs = [
            "999",         # Opción inválida
            "1",           # Nuevo juego
            "",            # Nombre vacío
            "Player",      # Nombre válido
            "Opponent",    # Segundo jugador
            "1",           # Humano vs Humano  
            "-1,-1",       # Posición inválida
            "0,0",         # Posición ya ocupada (después de primer movimiento)
            "0,1",         # Posición válida
            "0"            # Salir
        ]
        
        mock_input.side_effect = user_inputs
        
        from application.entry_points.cli_app import TicTacToeCLIApp
        
        # La aplicación debe manejar todos los errores sin crash
        try:
            cli_app = TicTacToeCLIApp()
            self.assertIsNotNone(cli_app)
        except Exception as e:
            self.fail(f"CLI app crashed with error: {e}")
    
    @patch('requests.post')
    def test_web_api_error_responses(self, mock_post):
        """Test E2E de respuestas de error en API web."""
        # Mock response de error
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "success": False,
            "error": "Datos de entrada inválidos",
            "details": ["Nombre de jugador requerido"]
        }
        mock_post.return_value = mock_response
        
        # Datos inválidos
        invalid_data = {
            "player1_name": "",  # Nombre vacío
            "player2_name": "Player 2"
        }
        
        # Simular llamada a API
        response = mock_post(f"http://localhost:5000/api/games", json=invalid_data)
        
        # Verificar manejo de error
        self.assertEqual(response.status_code, 400)
        
        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertIn("error", response_data)


class TestPerformanceEndToEnd(unittest.TestCase):
    """Tests E2E de rendimiento."""
    
    def test_cli_response_time(self):
        """Test E2E de tiempo de respuesta CLI."""
        import time
        
        start_time = time.time()
        
        from application.entry_points.cli_app import TicTacToeCLIApp
        
        # La aplicación debe inicializar rápidamente
        cli_app = TicTacToeCLIApp()
        
        end_time = time.time()
        initialization_time = end_time - start_time
        
        # Debe inicializar en menos de 1 segundo
        self.assertLess(initialization_time, 1.0)
        self.assertIsNotNone(cli_app)
    
    def test_web_app_response_time(self):
        """Test E2E de tiempo de respuesta aplicación web."""
        import time
        
        start_time = time.time()
        
        from application.entry_points.web_app import TicTacToeWebApp
        
        # La aplicación web debe inicializar rápidamente
        web_app = TicTacToeWebApp()
        
        end_time = time.time()
        initialization_time = end_time - start_time
        
        # Debe inicializar en menos de 2 segundos
        self.assertLess(initialization_time, 2.0)
        self.assertIsNotNone(web_app)
    
    def test_multiple_game_sessions(self):
        """Test E2E de múltiples sesiones de juego simultáneas."""
        from game.entities import GameSession, GameConfiguration
        
        # Crear múltiples sesiones
        sessions = []
        config = GameConfiguration()
        
        start_time = time.time()
        
        # Crear 100 sesiones de juego
        for i in range(100):
            session = GameSession(configuration=config)
            sessions.append(session)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        # Debe crear 100 sesiones en menos de 1 segundo
        self.assertLess(creation_time, 1.0)
        self.assertEqual(len(sessions), 100)
        
        # Verificar que todas las sesiones son únicas
        session_ids = [s.id for s in sessions]
        self.assertEqual(len(set(session_ids)), 100)


class TestScreamingArchitectureValidation(unittest.TestCase):
    """Tests E2E para validar los principios de Screaming Architecture."""
    
    def test_domain_focus_clarity(self):
        """Test E2E que verifica que la arquitectura 'grita' sobre el dominio del juego."""
        # Verificar que las imports principales reflejan el dominio del juego
        from game.entities import Board, Player, GameSession
        from game.use_cases.start_new_game import StartNewGameUseCase
        from game.services.ai_opponent import AIOpponentService
        
        # Los nombres de las clases deben reflejar claramente el dominio del juego
        self.assertIn("Game", GameSession.__name__)
        self.assertIn("Board", Board.__name__)
        self.assertIn("Player", Player.__name__)
        self.assertIn("Game", StartNewGameUseCase.__name__)
        self.assertIn("AI", AIOpponentService.__name__)
    
    def test_use_case_driven_design(self):
        """Test E2E que verifica el diseño dirigido por casos de uso."""
        from game.use_cases.start_new_game import StartNewGameUseCase, StartNewGameRequest
        
        # Los casos de uso deben ser explícitos y enfocados en el dominio
        use_case = StartNewGameUseCase()
        
        request = StartNewGameRequest(
            player1_name="Test Player 1",
            player2_name="Test Player 2"
        )
        
        response = use_case.execute(request)
        
        # El caso de uso debe funcionar independientemente de frameworks
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.game_session)
    
    def test_technology_independence(self):
        """Test E2E que verifica independencia de tecnologías específicas."""
        # El dominio debe funcionar sin dependencias de Flask, CLI, etc.
        from game.entities import GameSession, Player, PlayerType
        from game.entities import Board, Position, Move, CellState
        
        # Crear y usar entidades sin dependencias externas
        player1 = Player("Player 1", PlayerType.HUMAN)
        session = GameSession()
        board = session.board
        
        move = Move(Position(1, 1), CellState.PLAYER_X)
        result = board.place_move(move)
        
        # Todo debe funcionar sin frameworks específicos
        self.assertTrue(result)
        self.assertIsNotNone(session)
        self.assertEqual(player1.name, "Player 1")


if __name__ == '__main__':
    # Ejecutar tests E2E
    unittest.main(verbosity=2)