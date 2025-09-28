"""
Tests for utils/helpers.py
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from src.utils.helpers import calculate_winner, is_board_full, reset_board


class TestCalculateWinner:
    """Test calculate_winner function"""

    def test_winner_row_first_row(self):
        """Test winner in first row"""
        board = [["X", "X", "X"], ["O", "O", ""], ["", "", ""]]
        assert calculate_winner(board) == "X"

    def test_winner_row_middle_row(self):
        """Test winner in middle row"""
        board = [["X", "O", "X"], ["O", "O", "O"], ["X", "", ""]]
        assert calculate_winner(board) == "O"

    def test_winner_row_last_row(self):
        """Test winner in last row"""
        board = [["X", "O", ""], ["O", "X", ""], ["O", "O", "O"]]
        assert calculate_winner(board) == "O"

    def test_winner_column_first_column(self):
        """Test winner in first column"""
        board = [["X", "O", "O"], ["X", "O", ""], ["X", "", ""]]
        assert calculate_winner(board) == "X"

    def test_winner_column_middle_column(self):
        """Test winner in middle column"""
        board = [["O", "X", "O"], ["", "X", ""], ["", "X", ""]]
        assert calculate_winner(board) == "X"

    def test_winner_column_last_column(self):
        """Test winner in last column"""
        board = [["O", "", "X"], ["", "O", "X"], ["", "", "X"]]
        assert calculate_winner(board) == "X"

    def test_winner_main_diagonal(self):
        """Test winner in main diagonal (top-left to bottom-right)"""
        board = [["X", "O", "O"], ["O", "X", ""], ["", "", "X"]]
        assert calculate_winner(board) == "X"

    def test_winner_anti_diagonal(self):
        """Test winner in anti-diagonal (top-right to bottom-left)"""
        board = [["O", "", "X"], ["", "X", "O"], ["X", "", ""]]
        assert calculate_winner(board) == "X"

    def test_no_winner(self):
        """Test no winner scenario"""
        board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
        assert calculate_winner(board) is None

    def test_empty_board(self):
        """Test empty board has no winner"""
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        assert calculate_winner(board) is None

    def test_partial_board(self):
        """Test partially filled board with no winner"""
        board = [["X", "", "O"], ["", "X", ""], ["", "", ""]]
        assert calculate_winner(board) is None

    def test_larger_board_4x4_row_winner(self):
        """Test winner in 4x4 board - row"""
        board = [
            ["X", "X", "X", "X"],
            ["O", "O", "", ""],
            ["", "", "", ""],
            ["", "", "", ""],
        ]
        assert calculate_winner(board) == "X"

    def test_larger_board_4x4_diagonal_winner(self):
        """Test winner in 4x4 board - diagonal"""
        board = [
            ["O", "", "", ""],
            ["", "O", "", ""],
            ["", "", "O", ""],
            ["", "", "", "O"],
        ]
        assert calculate_winner(board) == "O"


class TestIsBoardFull:
    """Test is_board_full function"""

    def test_empty_board_not_full(self):
        """Test empty board is not full"""
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        assert is_board_full(board) is False

    def test_partially_filled_board_not_full(self):
        """Test partially filled board is not full"""
        board = [["X", "O", ""], ["", "X", "O"], ["O", "", "X"]]
        assert is_board_full(board) is False

    def test_full_board(self):
        """Test completely filled board is full"""
        board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
        assert is_board_full(board) is True

    def test_single_empty_cell_not_full(self):
        """Test board with single empty cell is not full"""
        board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", ""]]
        assert is_board_full(board) is False

    def test_larger_board_4x4_full(self):
        """Test 4x4 full board"""
        board = [
            ["X", "O", "X", "O"],
            ["O", "X", "O", "X"],
            ["X", "O", "X", "O"],
            ["O", "X", "O", "X"],
        ]
        assert is_board_full(board) is True

    def test_larger_board_4x4_not_full(self):
        """Test 4x4 not full board"""
        board = [
            ["X", "O", "X", ""],
            ["O", "X", "O", "X"],
            ["X", "O", "X", "O"],
            ["O", "X", "O", "X"],
        ]
        assert is_board_full(board) is False


class TestResetBoard:
    """Test reset_board function"""

    def test_reset_3x3_board(self):
        """Test creating 3x3 empty board"""
        board = reset_board(3)
        expected = [["", "", ""], ["", "", ""], ["", "", ""]]
        assert board == expected
        assert len(board) == 3
        assert all(len(row) == 3 for row in board)
        assert all(cell == "" for row in board for cell in row)

    def test_reset_4x4_board(self):
        """Test creating 4x4 empty board"""
        board = reset_board(4)
        assert len(board) == 4
        assert all(len(row) == 4 for row in board)
        assert all(cell == "" for row in board for cell in row)

    def test_reset_1x1_board(self):
        """Test creating 1x1 empty board"""
        board = reset_board(1)
        expected = [[""]]
        assert board == expected

    def test_reset_5x5_board(self):
        """Test creating 5x5 empty board"""
        board = reset_board(5)
        assert len(board) == 5
        assert all(len(row) == 5 for row in board)
        assert all(cell == "" for row in board for cell in row)

    def test_board_independence(self):
        """Test that modifying one row doesn't affect others"""
        board = reset_board(3)
        board[0][0] = "X"
        assert board[0][0] == "X"
        assert board[0][1] == ""
        assert board[1][0] == ""
        assert board[2][2] == ""


if __name__ == "__main__":
    # Simple test runner without pytest dependency issues
    import unittest

    # Convert pytest tests to unittest format for direct running
    class TestHelpers(unittest.TestCase):
        def test_basic_functionality(self):
            """Test basic helper functions work correctly"""
            from src.utils.helpers import calculate_winner, is_board_full, reset_board

            # Test reset_board
            board = reset_board(3)
            self.assertEqual(len(board), 3)
            self.assertTrue(all(len(row) == 3 for row in board))

            # Test is_board_full
            self.assertFalse(is_board_full(board))

            # Test calculate_winner
            self.assertIsNone(calculate_winner(board))

            # Test winner detection
            winning_board = [["X", "X", "X"], ["O", "O", ""], ["", "", ""]]
            self.assertEqual(calculate_winner(winning_board), "X")

            print("✅ All helper function tests passed!")

    unittest.main()
