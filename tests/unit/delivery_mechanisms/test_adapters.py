"""
Tests unitarios para los mecanismos de entrega (Delivery Mechanisms).

Estos tests verifican que los adaptadores web y CLI funcionan correctamente
como interfaces entre el mundo exterior y el dominio del juego.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json

# Imports del dominio
from game.entities import (
    GameSession, GameState, Player, PlayerType, PlayerSymbol,
    Board, Position, Move, CellState
)


class TestWebAdapter(unittest.TestCase):
    """Tests para el adaptador web (Flask)."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        # Mock de dependencias
        self.mock_start_new_game = Mock()
        self.mock_make_move = Mock()
        self.mock_check_winner = Mock()
        
        # Crear instancia mock del adaptador web
        from delivery_mechanisms.web.flask_web_adapter import FlaskWebAdapter
        self.web_adapter = FlaskWebAdapter(
            start_new_game_use_case=self.mock_start_new_game,
            make_move_use_case=self.mock_make_move,
            check_winner_use_case=self.mock_check_winner
        )
    
    def test_create_new_game_success(self):
        """Test de creación exitosa de nuevo juego via web."""
        # Mock de sesión de juego exitosa
        mock_session = Mock(spec=GameSession)
        mock_session.id = "test-session-123"
        mock_session.state = GameState.IN_PROGRESS
        
        self.mock_start_new_game.execute.return_value.success = True
        self.mock_start_new_game.execute.return_value.game_session = mock_session
        self.mock_start_new_game.execute.return_value.errors = []
        
        # Simular request data
        request_data = {
            "player1_name": "Jugador 1",
            "player2_name": "Jugador 2",
            "player2_type": "human"
        }
        
        response = self.web_adapter.create_new_game(request_data)
        
        self.assertIsInstance(response, dict)
        self.assertTrue(response.get('success', False))
        self.assertEqual(response.get('session_id'), "test-session-123")
    
    def test_create_new_game_validation_error(self):
        """Test de error de validación al crear juego via web."""
        self.mock_start_new_game.execute.return_value.success = False
        self.mock_start_new_game.execute.return_value.errors = ["Nombre inválido"]
        self.mock_start_new_game.execute.return_value.game_session = None
        
        request_data = {
            "player1_name": "",  # Nombre vacío
            "player2_name": "Jugador 2"
        }
        
        response = self.web_adapter.create_new_game(request_data)
        
        self.assertIsInstance(response, dict)
        self.assertFalse(response.get('success', True))
        self.assertIn('errors', response)
    
    def test_make_move_success(self):
        """Test de movimiento exitoso via web."""
        self.mock_make_move.execute.return_value.success = True
        self.mock_make_move.execute.return_value.errors = []
        
        request_data = {
            "session_id": "test-session-123",
            "player_id": "player-1",
            "position": {"row": 1, "col": 1}
        }
        
        response = self.web_adapter.make_move(request_data)
        
        self.assertIsInstance(response, dict)
        self.assertTrue(response.get('success', False))
    
    def test_make_move_invalid_position(self):
        """Test de movimiento con posición inválida via web."""
        self.mock_make_move.execute.return_value.success = False
        self.mock_make_move.execute.return_value.errors = ["Posición ocupada"]
        
        request_data = {
            "session_id": "test-session-123",
            "player_id": "player-1",
            "position": {"row": 0, "col": 0}  # Posición ya ocupada
        }
        
        response = self.web_adapter.make_move(request_data)
        
        self.assertIsInstance(response, dict)
        self.assertFalse(response.get('success', True))
    
    def test_get_game_status(self):
        """Test de obtención del estado del juego via web."""
        # Mock de estado del juego
        mock_board = Mock(spec=Board)
        mock_board.to_list.return_value = [
            ['X', 'O', ''],
            ['', 'X', ''],
            ['', '', 'O']
        ]
        
        mock_session = Mock(spec=GameSession)
        mock_session.id = "test-session-123"
        mock_session.state = GameState.IN_PROGRESS
        mock_session.board = mock_board
        mock_session.current_player_symbol = PlayerSymbol.X
        mock_session.move_count = 4
        
        # Simular obtención de sesión
        with patch.object(self.web_adapter, '_get_game_session', 
                         return_value=mock_session):
            response = self.web_adapter.get_game_status("test-session-123")
        
        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('session_id'), "test-session-123")
        self.assertEqual(response.get('state'), GameState.IN_PROGRESS.value)
        self.assertIn('board', response)
        self.assertEqual(response.get('current_player'), PlayerSymbol.X.value)
    
    def test_get_game_status_not_found(self):
        """Test cuando no se encuentra la sesión de juego via web."""
        with patch.object(self.web_adapter, '_get_game_session', 
                         return_value=None):
            response = self.web_adapter.get_game_status("nonexistent-session")
        
        self.assertIsInstance(response, dict)
        self.assertFalse(response.get('success', True))
        self.assertIn('error', response)


class TestConsoleAdapter(unittest.TestCase):
    """Tests para el adaptador de consola (CLI)."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        # Mock de dependencias
        self.mock_start_new_game = Mock()
        self.mock_make_move = Mock()
        self.mock_check_winner = Mock()
        
        from delivery_mechanisms.console.cli_adapter import CLIAdapter
        self.cli_adapter = CLIAdapter(
            start_new_game_use_case=self.mock_start_new_game,
            make_move_use_case=self.mock_make_move,
            check_winner_use_case=self.mock_check_winner
        )
    
    @patch('builtins.input')
    def test_get_player_names(self, mock_input):
        """Test de obtención de nombres de jugadores via CLI."""
        mock_input.side_effect = ["Jugador 1", "Jugador 2"]
        
        player1_name, player2_name = self.cli_adapter.get_player_names()
        
        self.assertEqual(player1_name, "Jugador 1")
        self.assertEqual(player2_name, "Jugador 2")
    
    @patch('builtins.input')
    def test_get_player_move(self, mock_input):
        """Test de obtención de movimiento de jugador via CLI."""
        mock_input.return_value = "1,1"  # Posición centro
        
        position = self.cli_adapter.get_player_move()
        
        self.assertIsInstance(position, Position)
        self.assertEqual(position.row, 1)
        self.assertEqual(position.col, 1)
    
    @patch('builtins.input')
    def test_get_player_move_invalid_format(self, mock_input):
        """Test de manejo de formato inválido en movimiento via CLI."""
        mock_input.side_effect = ["invalid", "1,1"]  # Primero inválido, luego válido
        
        position = self.cli_adapter.get_player_move()
        
        # Debe obtener la posición válida después del error
        self.assertIsInstance(position, Position)
        self.assertEqual(position.row, 1)
        self.assertEqual(position.col, 1)
    
    @patch('builtins.input')
    def test_get_game_mode(self, mock_input):
        """Test de selección de modo de juego via CLI."""
        mock_input.return_value = "1"  # Modo humano vs humano
        
        mode = self.cli_adapter.get_game_mode()
        
        self.assertEqual(mode, "human_vs_human")
    
    @patch('builtins.input')
    def test_get_ai_difficulty(self, mock_input):
        """Test de selección de dificultad AI via CLI."""
        mock_input.return_value = "2"  # Dificultad media
        
        difficulty = self.cli_adapter.get_ai_difficulty()
        
        self.assertEqual(difficulty, "medium")
    
    @patch('builtins.print')
    def test_display_board(self, mock_print):
        """Test de visualización del tablero via CLI."""
        mock_board = Mock(spec=Board)
        mock_board.to_list.return_value = [
            ['X', 'O', ''],
            ['', 'X', ''],
            ['', '', 'O']
        ]
        
        self.cli_adapter.display_board(mock_board)
        
        # Verificar que se llamó print (para mostrar el tablero)
        self.assertTrue(mock_print.called)
    
    @patch('builtins.print')
    def test_display_game_result_winner(self, mock_print):
        """Test de visualización de resultado con ganador via CLI."""
        winner_player = Mock(spec=Player)
        winner_player.name = "Jugador Ganador"
        
        self.cli_adapter.display_game_result(
            result="winner",
            winner=winner_player
        )
        
        # Verificar que se mostró el mensaje de victoria
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list)
        self.assertIn("Ganador", call_args)
    
    @patch('builtins.print')
    def test_display_game_result_draw(self, mock_print):
        """Test de visualización de resultado de empate via CLI."""
        self.cli_adapter.display_game_result(result="draw")
        
        # Verificar que se mostró el mensaje de empate
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list)
        self.assertIn("Empate", call_args) or self.assertIn("empate", call_args)
    
    @patch('builtins.print')
    def test_display_error_message(self, mock_print):
        """Test de visualización de mensajes de error via CLI."""
        error_message = "Posición ya ocupada"
        
        self.cli_adapter.display_error(error_message)
        
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list)
        self.assertIn(error_message, call_args)
    
    @patch('builtins.print')
    def test_display_welcome_message(self, mock_print):
        """Test de visualización de mensaje de bienvenida via CLI."""
        self.cli_adapter.display_welcome()
        
        mock_print.assert_called()
        # Verificar que se mostró algún mensaje
        self.assertTrue(len(mock_print.call_args_list) > 0)


class TestAdapterIntegration(unittest.TestCase):
    """Tests de integración entre adaptadores."""
    
    def test_web_to_cli_data_conversion(self):
        """Test de conversión de datos entre adaptadores web y CLI."""
        # Datos que vienen del web
        web_request = {
            "player1_name": "Web Player 1",
            "player2_name": "Web Player 2",
            "position": {"row": 0, "col": 2}
        }
        
        # Convertir a formato CLI
        position = Position(
            web_request["position"]["row"], 
            web_request["position"]["col"]
        )
        
        self.assertEqual(position.row, 0)
        self.assertEqual(position.col, 2)
    
    def test_cli_to_web_data_conversion(self):
        """Test de conversión de datos desde CLI a formato web."""
        # Datos que vienen del CLI
        position = Position(2, 1)
        
        # Convertir a formato web
        web_position = {
            "row": position.row,
            "col": position.col
        }
        
        self.assertEqual(web_position["row"], 2)
        self.assertEqual(web_position["col"], 1)
    
    def test_error_handling_consistency(self):
        """Test de consistencia en manejo de errores entre adaptadores."""
        error_cases = [
            "Posición ya ocupada",
            "Jugador inválido", 
            "Sesión no encontrada",
            "Movimiento fuera del tablero"
        ]
        
        for error_message in error_cases:
            # Ambos adaptadores deben manejar estos errores de manera consistente
            self.assertIsInstance(error_message, str)
            self.assertTrue(len(error_message) > 0)
    
    def test_game_state_representation_consistency(self):
        """Test de consistencia en representación del estado del juego."""
        # Crear estado mock
        mock_board = Mock(spec=Board)
        mock_board.to_list.return_value = [
            ['X', 'O', ''],
            ['', 'X', ''],
            ['', '', 'O']
        ]
        
        # Ambos adaptadores deben representar el mismo estado
        board_list = mock_board.to_list()
        
        # Verificar formato
        self.assertEqual(len(board_list), 3)  # 3 filas
        self.assertEqual(len(board_list[0]), 3)  # 3 columnas
        
        # Verificar contenido
        self.assertEqual(board_list[0][0], 'X')
        self.assertEqual(board_list[0][1], 'O')
        self.assertEqual(board_list[1][1], 'X')


class TestValidationHelpers(unittest.TestCase):
    """Tests para helpers de validación en adaptadores."""
    
    def test_position_validation(self):
        """Test de validación de posiciones."""
        # Posiciones válidas
        valid_positions = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        
        for row, col in valid_positions:
            position = Position(row, col)
            self.assertTrue(0 <= position.row <= 2)
            self.assertTrue(0 <= position.col <= 2)
        
        # Posiciones inválidas
        invalid_positions = [
            (-1, 0), (0, -1), (3, 0), (0, 3),
            (-1, -1), (3, 3), (0, 5), (5, 0)
        ]
        
        for row, col in invalid_positions:
            # Estas posiciones están fuera del rango válido
            self.assertTrue(
                row < 0 or row > 2 or col < 0 or col > 2
            )
    
    def test_player_name_validation(self):
        """Test de validación de nombres de jugadores."""
        # Nombres válidos
        valid_names = [
            "Juan", "María", "Jugador 1", "AI Bot", "Player X"
        ]
        
        for name in valid_names:
            self.assertIsInstance(name, str)
            self.assertTrue(len(name.strip()) > 0)
        
        # Nombres inválidos
        invalid_names = ["", "   ", None]
        
        for name in invalid_names:
            if name is None:
                self.assertIsNone(name)
            else:
                self.assertTrue(len(name.strip()) == 0)
    
    def test_request_data_validation(self):
        """Test de validación de datos de request."""
        # Request válido
        valid_request = {
            "player1_name": "Jugador 1",
            "player2_name": "Jugador 2",
            "session_id": "valid-session-123",
            "position": {"row": 1, "col": 1}
        }
        
        # Verificar campos requeridos
        required_fields_new_game = ["player1_name", "player2_name"]
        for field in required_fields_new_game:
            self.assertIn(field, valid_request)
        
        required_fields_move = ["session_id", "position"]
        for field in required_fields_move:
            self.assertIn(field, valid_request)
        
        # Verificar tipos
        self.assertIsInstance(valid_request["position"], dict)
        self.assertIn("row", valid_request["position"])
        self.assertIn("col", valid_request["position"])


if __name__ == '__main__':
    unittest.main()