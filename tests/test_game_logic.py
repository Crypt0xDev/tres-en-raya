import os
import sys
import unittest
from pathlib import Path

# Add project root to path for Screaming Architecture imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from game.entities.board import Board, Position, Move, CellState
from game.entities.player import Player


class TestGameLogic(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_board_state(self):
        """Test that the board starts empty"""
        for row in range(self.board.size):
            for col in range(self.board.size):
                position = Position(row, col)
                self.assertEqual(self.board.get_cell_state(position), CellState.EMPTY)

    def test_valid_move(self):
        """Test making a valid move"""
        position = Position(0, 0)
        move = Move(position, CellState.PLAYER_X)
        result = self.board.place_move(move)
        self.assertTrue(result)
        self.assertEqual(self.board.get_cell_state(position), CellState.PLAYER_X)

    def test_invalid_move(self):
        """Test making an invalid move on occupied cell"""
        position = Position(0, 0)
        move1 = Move(position, CellState.PLAYER_X)
        move2 = Move(position, CellState.PLAYER_O)
        
        self.board.place_move(move1)
        result = self.board.place_move(move2)
        self.assertFalse(result)

    def test_horizontal_winner(self):
        """Test horizontal winning condition"""
        # Create horizontal line for X
        for col in range(3):
            position = Position(0, col)
            move = Move(position, CellState.PLAYER_X)
            self.board.place_move(move)
        
        winner = self.board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_X)

    def test_vertical_winner(self):
        """Test vertical winning condition"""
        # Create vertical line for O
        for row in range(3):
            position = Position(row, 0)
            move = Move(position, CellState.PLAYER_O)
            self.board.place_move(move)
        
        winner = self.board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_O)

    def test_diagonal_winner(self):
        """Test diagonal winning condition"""
        # Create diagonal line for X
        for i in range(3):
            position = Position(i, i)
            move = Move(position, CellState.PLAYER_X)
            self.board.place_move(move)
        
        winner = self.board.get_winner()
        self.assertEqual(winner, CellState.PLAYER_X)

    def test_board_full(self):
        """Test board full condition (draw)"""
        # Fill board without winner: X O X / O X O / O X O
        moves = [
            (0, 0, CellState.PLAYER_X), (0, 1, CellState.PLAYER_O), (0, 2, CellState.PLAYER_X),
            (1, 0, CellState.PLAYER_O), (1, 1, CellState.PLAYER_X), (1, 2, CellState.PLAYER_O),
            (2, 0, CellState.PLAYER_O), (2, 1, CellState.PLAYER_X), (2, 2, CellState.PLAYER_O)
        ]
        
        for row, col, player in moves:
            position = Position(row, col)
            move = Move(position, player)
            self.board.place_move(move)
        
        self.assertTrue(self.board.is_full())

    def test_no_winner(self):
        """Test no winner condition"""
        winner = self.board.get_winner()
        self.assertIsNone(winner)


if __name__ == "__main__":
    unittest.main()
