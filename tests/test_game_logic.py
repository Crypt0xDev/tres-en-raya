import os
import sys
import unittest

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.core.board import Board
from src.core.player import Player
from src.interfaces.cli import game_logic


class TestGameLogic(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_board_state(self):
        """Test that the board starts empty"""
        for row in self.board.board:
            for cell in row:
                self.assertEqual(cell, " ")

    def test_valid_move(self):
        """Test making a valid move"""
        result = game_logic.make_move(self.board, "X", 0, 0)
        self.assertTrue(result)
        self.assertEqual(self.board.board[0][0], "X")

    def test_invalid_move(self):
        """Test making an invalid move on occupied cell"""
        game_logic.make_move(self.board, "X", 0, 0)
        result = game_logic.make_move(self.board, "O", 0, 0)
        self.assertFalse(result)

    def test_horizontal_winner(self):
        """Test horizontal winning condition"""
        self.board.board[0] = ["X", "X", "X"]
        winner = game_logic.check_winner(self.board)
        self.assertEqual(winner, "X")

    def test_vertical_winner(self):
        """Test vertical winning condition"""
        for i in range(3):
            self.board.board[i][0] = "O"
        winner = game_logic.check_winner(self.board)
        self.assertEqual(winner, "O")

    def test_diagonal_winner(self):
        """Test diagonal winning condition"""
        for i in range(3):
            self.board.board[i][i] = "X"
        winner = game_logic.check_winner(self.board)
        self.assertEqual(winner, "X")

    def test_board_full(self):
        """Test board full condition (draw)"""
        test_board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
        self.board.board = test_board
        self.assertTrue(game_logic.is_board_full(self.board))

    def test_no_winner(self):
        """Test no winner condition"""
        winner = game_logic.check_winner(self.board)
        self.assertIsNone(winner)


if __name__ == "__main__":
    unittest.main()
