import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from multiplayer.client import MultiplayerClient
from core.game_engine import GameEngine

class MultiplayerTestCase(unittest.TestCase):
    def setUp(self):
        self.game_engine = GameEngine()
        self.client = MultiplayerClient()

    def test_game_engine_multiplayer(self):
        """Test game engine functionality for multiplayer"""
        # Start a new game
        game_id = self.game_engine.start_game("Alice", "Bob")
        self.assertIsNotNone(game_id)
        
        # Check initial game status
        status = self.game_engine.get_game_status(game_id)
        self.assertEqual(status['status'], 'active')
        self.assertEqual(status['current_player'], 'Alice')

    def test_multiplayer_moves(self):
        """Test making moves in multiplayer game"""
        game_id = self.game_engine.start_game("Alice", "Bob")
        
        # Alice makes first move
        result = self.game_engine.make_move(game_id, "Alice", 4)  # Center position
        self.assertTrue(result['success'])
        
        # Check it's now Bob's turn
        status = self.game_engine.get_game_status(game_id)
        self.assertEqual(status['current_player'], 'Bob')

    def test_invalid_move(self):
        """Test invalid moves in multiplayer"""
        game_id = self.game_engine.start_game("Alice", "Bob")
        
        # Bob tries to move when it's Alice's turn
        result = self.game_engine.make_move(game_id, "Bob", 0)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Not your turn')

    def test_game_completion(self):
        """Test game completion detection"""
        game_id = self.game_engine.start_game("Alice", "Bob")
        
        # Simulate a winning sequence for Alice (X)
        moves = [
            ("Alice", 0),  # X
            ("Bob", 1),    # O  
            ("Alice", 3),  # X
            ("Bob", 2),    # O
            ("Alice", 6)   # X wins (0,3,6 column)
        ]
        
        for i, (player, position) in enumerate(moves):
            result = self.game_engine.make_move(game_id, player, position)
            if i == len(moves) - 1:  # Last move should win
                self.assertTrue(result['success'])
                self.assertEqual(result['winner'], 'X')
            else:
                self.assertTrue(result['success'])

    @patch('socket.socket')
    def test_client_connection(self, mock_socket):
        """Test client connection functionality"""
        import socket
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        
        # Test that socket is created with correct parameters
        client = MultiplayerClient()
        
        # Verify socket was created with correct parameters
        mock_socket.assert_called_with(
            socket.AF_INET, 
            socket.SOCK_STREAM
        )

    def test_game_not_found(self):
        """Test error handling for non-existent games"""
        result = self.game_engine.make_move("nonexistent", "Alice", 0)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Game not found')

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()