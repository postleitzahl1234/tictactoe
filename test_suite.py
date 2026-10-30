#!/usr/bin/env python3
"""
Comprehensive test suite for Tic Tac Toe game application.
Tests all core game logic, AI, file I/O, and GUI components.
"""

import unittest
import json
import os
import sys
import tempfile
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add GUI to path
sys.path.insert(0, os.path.dirname(__file__))

from GUI.main import TicTacToe, MegaTicTacToe
from GUI.handlers import InputHandler
import pygame
from GUI.constants import THEMES, WINDOW_WIDTH, WINDOW_HEIGHT


class TestTicTacToeGameLogic(unittest.TestCase):
    """Test basic Tic Tac Toe game logic."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = TicTacToe("Player 1", "Player 2", "X", "O")
    
    def test_board_initialization(self):
        """Test that board initializes correctly."""
        self.assertEqual(len(self.game.board), 3)
        for row in self.game.board:
            self.assertEqual(len(row), 3)
            for cell in row:
                self.assertEqual(cell, " ")
    
    def test_active_player_initialization(self):
        """Test that active player initializes correctly."""
        self.assertEqual(self.game.active_player, 1)
        self.assertEqual(self.game.active_symbol, "X")
    
    def test_set_starting_position(self):
        """Test that starting position sets correctly."""
        self.game.set_starting_position()
        self.assertEqual(self.game.move_count, 0)
        self.assertEqual(self.game.active_player, 1)
        # Verify board is cleared
        for row in self.game.board:
            for cell in row:
                self.assertEqual(cell, " ")
    
    def test_change_active_player(self):
        """Test player alternation."""
        self.assertEqual(self.game.active_player, 1)
        self.game.change_active_player()
        self.assertEqual(self.game.active_player, 2)
        self.assertEqual(self.game.active_symbol, "O")
        self.game.change_active_player()
        self.assertEqual(self.game.active_player, 1)
        self.assertEqual(self.game.active_symbol, "X")
    
    def test_horizontal_win(self):
        """Test detection of horizontal wins."""
        # Player 1 (X) wins with top row
        self.game.board[0][0] = "X"
        self.game.board[0][1] = "X"
        self.game.board[0][2] = "X"
        self.assertEqual(self.game.is_winning(), "X")
    
    def test_vertical_win(self):
        """Test detection of vertical wins."""
        # Player 2 (O) wins with middle column
        self.game.board[0][1] = "O"
        self.game.board[1][1] = "O"
        self.game.board[2][1] = "O"
        self.assertEqual(self.game.is_winning(), "O")
    
    def test_diagonal_win_topleft_to_bottomright(self):
        """Test diagonal win (top-left to bottom-right)."""
        self.game.board[0][0] = "X"
        self.game.board[1][1] = "X"
        self.game.board[2][2] = "X"
        self.assertEqual(self.game.is_winning(), "X")
    
    def test_diagonal_win_topright_to_bottomleft(self):
        """Test diagonal win (top-right to bottom-left)."""
        self.game.board[0][2] = "O"
        self.game.board[1][1] = "O"
        self.game.board[2][0] = "O"
        self.assertEqual(self.game.is_winning(), "O")
    
    def test_no_win(self):
        """Test that no win is detected when appropriate."""
        self.game.board[0][0] = "X"
        self.game.board[0][1] = "O"
        self.game.board[1][1] = "X"
        self.assertIsNone(self.game.is_winning())
    
    def test_register_win(self):
        """Test win registration."""
        self.assertEqual(self.game.win_counts["Player 1"], 0)
        winner_name = self.game.register_win("X")
        self.assertEqual(winner_name, "Player 1")
        self.assertEqual(self.game.win_counts["Player 1"], 1)
    
    def test_get_available_moves(self):
        """Test available moves detection."""
        moves = self.game.get_available_moves()
        self.assertEqual(len(moves), 9)
        
        # Fill some cells
        self.game.board[0][0] = "X"
        self.game.board[1][1] = "O"
        moves = self.game.get_available_moves()
        self.assertEqual(len(moves), 7)
    
    def test_get_winner_name(self):
        """Test winner name retrieval."""
        self.assertEqual(self.game.get_winner_name("X"), "Player 1")
        self.assertEqual(self.game.get_winner_name("O"), "Player 2")
        self.assertEqual(self.game.get_winner_name("Z"), "Unknown")
    
    def test_current_player_name(self):
        """Test current player name."""
        self.assertEqual(self.game.current_player_name(), "Player 1")
        self.game.active_player = 2
        self.assertEqual(self.game.current_player_name(), "Player 2")


class TestBotAI(unittest.TestCase):
    """Test bot AI algorithms."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = TicTacToe("Player 1", "Player 2", "X", "O")
        self.game.game_mode = 'singleplayer'
    
    def test_easy_bot_move(self):
        """Test that easy bot returns a valid move."""
        moves = self.game.get_available_moves()
        initial_count = len(moves)
        
        r, c = self.game.get_bot_move(difficulty='easy')
        self.assertIsNotNone(r)
        self.assertIsNotNone(c)
        self.assertTrue(0 <= r < 3 and 0 <= c < 3)
    
    def test_medium_bot_tries_to_win(self):
        """Test that medium bot tries to win."""
        # Set up board where bot can win
        self.game.board[0][0] = "O"
        self.game.board[0][1] = "O"
        self.game.board[0][2] = " "
        
        r, c = self.game.get_bot_move(difficulty='medium')
        self.assertEqual((r, c), (0, 2))
    
    def test_medium_bot_blocks_opponent(self):
        """Test that medium bot blocks opponent win."""
        # Set up board where opponent can win
        self.game.board[1][0] = "X"
        self.game.board[1][1] = "X"
        self.game.board[1][2] = " "
        
        r, c = self.game.get_bot_move(difficulty='medium')
        self.assertEqual((r, c), (1, 2))
    
    def test_hard_bot_move(self):
        """Test that hard bot returns a valid move."""
        # Hard bot uses minimax
        r, c = self.game.get_bot_move(difficulty='hard')
        self.assertIsNotNone(r)
        self.assertIsNotNone(c)
        # On an empty board every move draws with perfect play, so any free cell is fine
        self.assertIn((r, c), [(i, j) for i in range(3) for j in range(3)])

    def test_hard_bot_blocks_win(self):
        """Hard bot (O) must block X's open row."""
        self.game.board[0][0] = "X"
        self.game.board[0][1] = "X"
        self.game.board[1][1] = "O"
        self.assertEqual(self.game.get_bot_move(difficulty='hard'), (0, 2))
    
    def test_bot_no_moves_available(self):
        """Test bot when no moves are available."""
        # Fill entire board
        for i in range(3):
            for j in range(3):
                self.game.board[i][j] = "X" if (i + j) % 2 == 0 else "O"
        
        r, c = self.game.get_bot_move(difficulty='easy')
        self.assertIsNone(r)
        self.assertIsNone(c)


class TestMegaTicTacToe(unittest.TestCase):
    """Test Mega Tic Tac Toe game logic."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = MegaTicTacToe("Player 1", "Player 2", "X", "O")
    
    def test_mega_board_initialization(self):
        """Test that mega board initializes correctly."""
        self.assertEqual(len(self.game.board), 3)
        for mega_row in self.game.board:
            self.assertEqual(len(mega_row), 3)
            for board in mega_row:
                self.assertEqual(len(board), 3)
                for row in board:
                    self.assertEqual(len(row), 3)
                    for cell in row:
                        self.assertEqual(cell, " ")
    
    def test_mega_claimed_boards_initialization(self):
        """Test that claimed boards initialize correctly."""
        self.assertEqual(len(self.game.claimed_boards), 3)
        for row in self.game.claimed_boards:
            self.assertEqual(len(row), 3)
            for cell in row:
                self.assertEqual(cell, " ")
    
    def test_mega_available_moves(self):
        """Test available moves in mega game."""
        # Initially all 9 small boards and all 9 cells of each are available
        self.assertEqual(len(self.game.get_available_small_boards()), 9)
        self.assertEqual(len(self.game.get_available_moves_in_board(0, 0)), 9)
    
    def test_mega_win_condition(self):
        """Test mega game win detection."""
        # Set up a winning pattern on the meta board
        self.game.claimed_boards[0][0] = "X"
        self.game.claimed_boards[0][1] = "X"
        self.game.claimed_boards[0][2] = "X"
        self.game.claimed_boards[1][0] = "O"
        self.game.claimed_boards[1][1] = "O"

        winner = self.game.check_mega_winner()
        self.assertEqual(winner, "X")
    
    def test_mega_get_winner_name(self):
        """Test winner name in mega game."""
        name = self.game.get_winner_name("X")
        self.assertEqual(name, "Player 1")


class TestFileIO(unittest.TestCase):
    """Test file I/O operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = TicTacToe("Player 1", "Player 2", "X", "O")
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_write_game_result(self):
        """Test game result file writing."""
        result_file = os.path.join(self.temp_dir, 'test_results.txt')
        
        # Win a game
        self.game.board[0][0] = "X"
        self.game.board[0][1] = "X"
        self.game.board[0][2] = "X"
        
        self.game.write_game_result("X", result_file)
        
        # Verify file exists
        self.assertTrue(os.path.exists(result_file))
        
        # Verify content
        with open(result_file, 'r') as f:
            content = f.read()
            self.assertIn("Winner: X", content)
            self.assertIn("Player 1", content)


class TestInputHandler(unittest.TestCase):
    """Test input handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = InputHandler()
    
    def test_input_handler_initialization(self):
        """Test that input handler initializes."""
        self.assertIsNotNone(self.handler)
    
    def test_screen_to_board_coordinates(self):
        """Test screen coordinate to board coordinate conversion."""
        # Test valid coordinates - these will depend on screen constants
        # This is a basic sanity check
        pygame.display.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # The centre of the window is the centre cell
        self.assertEqual(self.handler.get_cell_from_click((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)), (1, 1))
        # A click in the corner of the window is outside the board
        self.assertEqual(self.handler.get_cell_from_click((0, 0)), (None, None))


class TestThemeConstants(unittest.TestCase):
    """Test theme constants."""
    
    def test_available_themes(self):
        """Test that required themes are available."""
        required_themes = ['forest', 'soft desert', 'misty pastel', 'ocean breeze']
        for theme in required_themes:
            self.assertIn(theme, THEMES)
    
    def test_theme_structure(self):
        """Test that themes have required color keys."""
        required_keys = ['bg', 'line', 'circle', 'cross', 'text', 'button', 'button_hover']
        for theme_name, theme_colors in THEMES.items():
            for key in required_keys:
                self.assertIn(key, theme_colors, f"Theme {theme_name} missing {key}")


class TestGameFlow(unittest.TestCase):
    """Test complete game flow scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = TicTacToe("Player 1", "Player 2", "X", "O")
    
    def test_alternating_turns(self):
        """Test that players alternate correctly."""
        self.game.set_starting_position()
        
        # Simulate a game with alternating moves
        moves = [
            (0, 0), (0, 1), (1, 1),  # X, O, X
            (1, 0), (2, 2), (0, 2)   # O (block), O (win?)
        ]
        
        player_sequence = []
        for r, c in moves[:3]:
            if self.game.board[r][c] == " ":
                self.game.board[r][c] = self.game.active_symbol
                player_sequence.append(self.game.active_player)
                self.game.move_count += 1
                self.game.change_active_player()
        
        # Should be 1, 2, 1 (X, O, X)
        self.assertEqual(player_sequence, [1, 2, 1])
    
    def test_starting_player_alternation(self):
        """Test that starting player alternates between games."""
        self.game.set_starting_position()
        first_starter = self.game.active_player
        self.game.set_starting_position()
        
        # The next game is started by the other player
        self.assertNotEqual(self.game.active_player, first_starter)


class TestFormatBoard(unittest.TestCase):
    """Test board formatting."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = TicTacToe("Player 1", "Player 2", "X", "O")
    
    def test_format_empty_board(self):
        """Test formatting of empty board."""
        formatted = self.game.format_board()
        self.assertIn("|", formatted)
        self.assertIn(" ", formatted)
    
    def test_format_filled_board(self):
        """Test formatting of filled board."""
        self.game.board[0][0] = "X"
        self.game.board[0][1] = "O"
        self.game.board[1][1] = "X"
        
        formatted = self.game.format_board()
        self.assertIn("X", formatted)
        self.assertIn("O", formatted)
    
    def test_show_board(self):
        """Test board display (capture stdout)."""
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            self.game.show_board()
        
        output = f.getvalue()
        self.assertIn("|", output)
        self.assertIn("-", output)


def run_comprehensive_test_suite():
    """Run all tests with detailed output."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTicTacToeGameLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestBotAI))
    suite.addTests(loader.loadTestsFromTestCase(TestMegaTicTacToe))
    suite.addTests(loader.loadTestsFromTestCase(TestFileIO))
    suite.addTests(loader.loadTestsFromTestCase(TestInputHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestThemeConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestGameFlow))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatBoard))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_comprehensive_test_suite()
    sys.exit(0 if result.wasSuccessful() else 1)
