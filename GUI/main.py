from datetime import datetime
import json
import os
import random


class TicTacToe:
    def __init__(self, name1, name2, symbol1, symbol2):
        self.name1 = name1
        self.name2 = name2
        self.symbol1 = symbol1
        self.symbol2 = symbol2
        # board rows: 0 = top, 2 = bottom
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.active_player = 1
        # track who should start the next game; toggled each new game so the starter alternates
        self.starting_player = 1
        self.active_symbol = self.symbol1
        self.move_count = 0
        # track number of wins per player
        self.win_counts = {self.name1: 0, self.name2: 0}
        # game mode: 'multiplayer' or 'singleplayer' (UI toggles this; singleplayer uses a bot)
        self.game_mode = 'multiplayer'
        # bot difficulty: 'easy','medium','hard' (used when in singleplayer mode)
        self.bot_difficulty = 'medium'

    def play_single_game(self):
        self.set_starting_position()
        self.show_board()
        while True:
            self.set_tile()
            self.show_board()
            winner_symbol = self.is_winning()
            if winner_symbol:
                # register and announce winner
                winner_name = self.register_win(winner_symbol)
                print(f"{winner_name} has won the game!")
                # persist updated scores
                try:
                    self.write_scores_to_file()
                except Exception:
                    pass
                # append game result log
                try:
                    self.write_game_result(winner_symbol)
                except Exception:
                    pass
                break
            if self.move_count >= 9:
                print("Game is a draw.")
                try:
                    self.write_scores_to_file()
                except Exception:
                    pass
                try:
                    self.write_game_result(None)
                except Exception:
                    pass
                break
            self.change_active_player()

    def game_loop(self):
        while True:
            self.play_single_game()
            while True:
                play_again = input("\nPlay again? (yes/no): ").strip().lower()
                if play_again in ['yes', 'y']:
                    break
                elif play_again in ['no', 'n', 'quit', 'q']:
                    print("Thanks for playing!")
                    # write final scores
                    try:
                        self.write_scores_to_file()
                    except Exception:
                        pass
                    return
                else:
                    print("Please enter 'yes' or 'no'.")

    def set_starting_position(self):
        # Set active player to the configured starting_player, then flip it for the next game
        self.active_player = self.starting_player
        self.active_symbol = self.symbol1 if self.active_player == 1 else self.symbol2
        # flip starting player so a different player begins each time
        self.starting_player = 2 if self.starting_player == 1 else 1
        self.move_count = 0
        # reset/clear the board for a new game
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def register_win(self, winner_symbol):
        """Increment win counter for the player who used winner_symbol and return their name."""
        if winner_symbol == self.symbol1:
            winner_name = self.name1
        elif winner_symbol == self.symbol2:
            winner_name = self.name2
        else:
            winner_name = "Unknown"

        # initialize key if names changed dynamically
        if winner_name not in self.win_counts:
            self.win_counts[winner_name] = 0

        self.win_counts[winner_name] += 1
        return winner_name

    def write_scores_to_file(self, path='scores.txt'):
        """File I/O disabled for performance."""
        pass

    def format_board(self):
        """Return a simple multi-line string representation of the current board with spaces for empty tiles."""
        lines = []
        for row in self.board:
            lines.append('| ' + ' | '.join(cell if cell != ' ' else ' ' for cell in row) + ' |')
        return '\n'.join(lines)

    def write_game_result(self, winner_symbol, path='game_results.txt'):
        """Write game result to file with timestamp."""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            winner = "Draw" if winner_symbol is None else f"Winner: {winner_symbol} ({self.get_winner_name(winner_symbol)})"
            
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} - {winner}\n")
                f.write(f"{self.name1} ({self.symbol1}) vs {self.name2} ({self.symbol2})\n")
                f.write("\n")
                f.write(self.format_board())
                f.write("\n")
                f.write("\n---\n\n")
            print(f"Game result written to {path}")
        except Exception as e:
            print(f"Error writing game result to {path}: {e}")

    def get_winner_name(self, symbol):
        """Get the name of the player with the given symbol."""
        if symbol == self.symbol1:
            return self.name1
        elif symbol == self.symbol2:
            return self.name2
        return "Unknown"

    def show_board(self):
        print("-------------")
        print(f"| {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]} |")
        print("-------------")
        print(f"| {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]} |")
        print("-------------")
        print(f"| {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]} |")
        print("-------------")

    def change_active_player(self):
        if self.active_player == 1:
            self.active_player = 2
            self.active_symbol = self.symbol2
        else:
            self.active_player = 1
            self.active_symbol = self.symbol1

    def set_tile(self):
        # Expect coordinates as: x y where x and y are 1..3
        while True:
            user = input(f"{self.current_player_name()} ({self.active_symbol}), type coordinates x y (1-3): ")
            parts = user.strip().split()
            if len(parts) != 2:
                print("Please enter two numbers separated by space, e.g. '1 3'")
                continue
            try:
                x = int(parts[0])
                y = int(parts[1])
            except ValueError:
                print("Coordinates must be integers.")
                continue
            if not (1 <= x <= 3 and 1 <= y <= 3):
                print("Coordinates must be between 1 and 3.")
                continue
            # Convert (x,y) where y=3 is top row, to board indices
            row = 3 - y
            col = x - 1
            if self.board[row][col] != " ":
                print("That tile is already taken. Choose another.")
                continue
            self.board[row][col] = self.active_symbol
            self.move_count += 1
            break

    def get_available_moves(self):
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == ' ':
                    moves.append((r, c))
        return moves

    def get_bot_move(self, difficulty='medium'):
        """Return (row,col) for the bot move according to difficulty."""
        bot_sym = self.symbol2
        opp_sym = self.symbol1
        moves = self.get_available_moves()
        if not moves:
            return None, None

        if difficulty == 'easy':
            return random.choice(moves)

        # medium: try win, then block, else random
        for r, c in moves:
            self.board[r][c] = bot_sym
            if self.is_winning() == bot_sym:
                self.board[r][c] = ' '
                return r, c
            self.board[r][c] = ' '
        for r, c in moves:
            self.board[r][c] = opp_sym
            if self.is_winning() == opp_sym:
                self.board[r][c] = ' '
                return r, c
            self.board[r][c] = ' '

        if difficulty == 'medium':
            return random.choice(moves)

        # hard: minimax
        best_score = -999
        best_move = None

        def minimax(is_maximizing):
            winner = self.is_winning()
            if winner == bot_sym:
                return 1
            elif winner == opp_sym:
                return -1
            elif not self.get_available_moves():
                return 0

            if is_maximizing:
                max_eval = -999
                for (rr, cc) in self.get_available_moves():
                    self.board[rr][cc] = bot_sym
                    eval = minimax(False)
                    self.board[rr][cc] = ' '
                    max_eval = max(max_eval, eval)
                return max_eval
            else:
                min_eval = 999
                for (rr, cc) in self.get_available_moves():
                    self.board[rr][cc] = opp_sym
                    eval = minimax(True)
                    self.board[rr][cc] = ' '
                    min_eval = min(min_eval, eval)
                return min_eval

        for (r, c) in moves:
            self.board[r][c] = bot_sym
            score = minimax(False)
            self.board[r][c] = ' '
            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move if best_move is not None else random.choice(moves)

    def is_winning(self):
        b = self.board
        winner_symbol = None
        # rows and columns
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] and b[i][0] != " ":
                winner_symbol = b[i][0]
                break
            if b[0][i] == b[1][i] == b[2][i] and b[0][i] != " ":
                winner_symbol = b[0][i]
                break
        # diagonals
        if winner_symbol is None:
            if b[0][0] == b[1][1] == b[2][2] and b[0][0] != " ":
                winner_symbol = b[0][0]
            elif b[0][2] == b[1][1] == b[2][0] and b[0][2] != " ":
                winner_symbol = b[0][2]

        return winner_symbol

    def current_player_name(self):
        return self.name1 if self.active_player == 1 else self.name2


class MegaTicTacToe(TicTacToe):
    """Mega Tic Tac Toe: 9 tictactoe boards arranged in a 3x3 grid.
    
    Uses a unified 3D board structure: board[mega_row][mega_col][cell_row][cell_col]
    where mega_row, mega_col ∈ [0,1,2] specify which small board
    and cell_row, cell_col ∈ [0,1,2] specify the cell within that board.
    """
    
    def __init__(self, name1, name2, symbol1, symbol2):
        super().__init__(name1, name2, symbol1, symbol2)
        # 3D board: board[mega_row][mega_col][cell_row][cell_col]
        self.board = [[[[" " for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        # claimed_boards[mega_row][mega_col] = symbol or "D" for draw or " " for unclaimed
        self.claimed_boards = [[" " for _ in range(3)] for _ in range(3)]
        
        # Track active small board (which board must be played on next)
        # None means player can choose any available board
        self.active_board = None
        self.total_moves = 0

    def set_starting_position(self):
        """Reset mega game state."""
        self.active_player = self.starting_player
        self.active_symbol = self.symbol1 if self.active_player == 1 else self.symbol2
        self.starting_player = 2 if self.starting_player == 1 else 1
        self.total_moves = 0
        
        # Reset all boards
        self.board = [[[[" " for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.claimed_boards = [[" " for _ in range(3)] for _ in range(3)]
        self.active_board = None
        self.move_count = 0

    def get_available_small_boards(self):
        """Return list of (row, col) for unclaimed small boards."""
        boards = []
        for r in range(3):
            for c in range(3):
                if self.claimed_boards[r][c] == " ":
                    boards.append((r, c))
        return boards

    def get_available_moves_in_board(self, board_row, board_col):
        """Get available (row, col) in a specific small board."""
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[board_row][board_col][r][c] == " ":
                    moves.append((r, c))
        return moves

    def _quick_board_check(self, br, bc, symbol):
        """Fast inline win check for bot evaluation. Only checks if symbol wins (not full check)."""
        board = self.board[br][bc]
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] == symbol:
                return True
            if board[0][i] == board[1][i] == board[2][i] == symbol:
                return True
        if board[0][0] == board[1][1] == board[2][2] == symbol:
            return True
        if board[0][2] == board[1][1] == board[2][0] == symbol:
            return True
        return False

    def _quick_mega_check(self, symbol):
        """Fast inline mega win check for bot evaluation. Only checks if symbol wins."""
        for i in range(3):
            if self.claimed_boards[i][0] == self.claimed_boards[i][1] == self.claimed_boards[i][2] == symbol:
                return True
            if self.claimed_boards[0][i] == self.claimed_boards[1][i] == self.claimed_boards[2][i] == symbol:
                return True
        if self.claimed_boards[0][0] == self.claimed_boards[1][1] == self.claimed_boards[2][2] == symbol:
            return True
        if self.claimed_boards[0][2] == self.claimed_boards[1][1] == self.claimed_boards[2][0] == symbol:
            return True
        return False

    def check_small_board_winner(self, board_row, board_col):
        """Check if a small board has a winner. Return symbol or None or "D" for draw."""
        board = self.board[board_row][board_col]
        
        # Count filled cells
        filled = sum(1 for row in board for cell in row if cell != " ")
        
        # Can't win until at least 5 moves in a small board
        if filled < 5:
            return None
        
        # Check rows/cols for three in a row
        for i in range(3):
            # Check row
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] != " ":
                return board[i][0]
            # Check column
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] != " ":
                return board[0][i]
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
            return board[0][2]
        
        # Check if board is full (draw)
        if filled == 9:
            return "D"
        
        return None

    def check_mega_winner(self):
        """Check if mega board has a winner. Return symbol or None or "D"."""
        # Can't win until at least 5 small boards are claimed
        claimed = sum(1 for row in self.claimed_boards for cell in row if cell != " ")
        if claimed < 5:
            return None
        
        # Check rows/cols
        for i in range(3):
            if self.claimed_boards[i][0] == self.claimed_boards[i][1] == self.claimed_boards[i][2] and self.claimed_boards[i][0] != " ":
                return self.claimed_boards[i][0]
            if self.claimed_boards[0][i] == self.claimed_boards[1][i] == self.claimed_boards[2][i] and self.claimed_boards[0][i] != " ":
                return self.claimed_boards[0][i]
        # Check diagonals
        if self.claimed_boards[0][0] == self.claimed_boards[1][1] == self.claimed_boards[2][2] and self.claimed_boards[0][0] != " ":
            return self.claimed_boards[0][0]
        if self.claimed_boards[0][2] == self.claimed_boards[1][1] == self.claimed_boards[2][0] and self.claimed_boards[0][2] != " ":
            return self.claimed_boards[0][2]
        
        # Check if all cells claimed
        if claimed == 9:
            return "D"
        return None

    def play_move_in_board(self, board_row, board_col, cell_row, cell_col):
        """Play a move in a specific small board. Return True if valid."""
        # Validate parameters
        if not (0 <= board_row < 3 and 0 <= board_col < 3 and 
                0 <= cell_row < 3 and 0 <= cell_col < 3):
            return False
        
        # Check if mega board cell is already won/drawn
        if self.claimed_boards[board_row][board_col] != " ":
            return False
        
        # Check if cell is free
        if self.board[board_row][board_col][cell_row][cell_col] != " ":
            return False
        
        # Check if board is active (if one was designated)
        if self.active_board is not None:
            if (board_row, board_col) != self.active_board:
                return False
        
        # Make the move
        self.board[board_row][board_col][cell_row][cell_col] = self.active_symbol
        self.total_moves += 1
        self.move_count += 1
        
        # Check if this small board is now won/drawn - this is critical
        winner = self.check_small_board_winner(board_row, board_col)
        if winner is not None:
            # Mark the board as claimed immediately
            self.claimed_boards[board_row][board_col] = winner
            # Ensure we can't play in this board anymore
            assert self.claimed_boards[board_row][board_col] != " ", f"Board {board_row},{board_col} should be marked as {winner}"
        
        # Determine next active board based on cell position
        next_board = (cell_row, cell_col)
        if self.claimed_boards[next_board[0]][next_board[1]] != " ":
            # That board is already claimed, can play anywhere available
            self.active_board = None
        else:
            self.active_board = next_board
        
        return True

    def get_bot_move_mega(self, difficulty='medium'):
        """Return (board_row, board_col, cell_row, cell_col) for mega tictactoe bot."""
        bot_sym = self.symbol2
        opp_sym = self.symbol1
        
        # Get valid boards
        if self.active_board is not None:
            valid_boards = [self.active_board]
        else:
            valid_boards = self.get_available_small_boards()
        
        all_moves = []
        for br, bc in valid_boards:
            moves = self.get_available_moves_in_board(br, bc)
            for mr, mc in moves:
                all_moves.append((br, bc, mr, mc))
        
        if not all_moves:
            return None
        
        if difficulty == 'easy':
            return random.choice(all_moves)
        
        # medium: try to win small board, block opponent, try to win mega, block mega, else random
        for br, bc, mr, mc in all_moves:
            self.board[br][bc][mr][mc] = bot_sym
            if self._quick_board_check(br, bc, bot_sym):
                self.board[br][bc][mr][mc] = " "
                return (br, bc, mr, mc)
            self.board[br][bc][mr][mc] = " "
        
        for br, bc, mr, mc in all_moves:
            self.board[br][bc][mr][mc] = opp_sym
            if self._quick_board_check(br, bc, opp_sym):
                self.board[br][bc][mr][mc] = " "
                return (br, bc, mr, mc)
            self.board[br][bc][mr][mc] = " "
        
        if difficulty == 'medium':
            return random.choice(all_moves)
        
        # hard: simplified strategy without minimax (too slow for mega)
        # Try to win mega board
        for br, bc, mr, mc in all_moves:
            if self.claimed_boards[br][bc] == " ":
                self.board[br][bc][mr][mc] = bot_sym
                if self._quick_board_check(br, bc, bot_sym):
                    self.claimed_boards[br][bc] = bot_sym
                    if self._quick_mega_check(bot_sym):
                        self.claimed_boards[br][bc] = " "
                        self.board[br][bc][mr][mc] = " "
                        return (br, bc, mr, mc)
                    self.claimed_boards[br][bc] = " "
                self.board[br][bc][mr][mc] = " "
        
        # Block opponent from winning mega board
        for br, bc, mr, mc in all_moves:
            if self.claimed_boards[br][bc] == " ":
                self.board[br][bc][mr][mc] = opp_sym
                if self._quick_board_check(br, bc, opp_sym):
                    self.claimed_boards[br][bc] = opp_sym
                    if self._quick_mega_check(opp_sym):
                        self.claimed_boards[br][bc] = " "
                        self.board[br][bc][mr][mc] = " "
                        return (br, bc, mr, mc)
                    self.claimed_boards[br][bc] = " "
                self.board[br][bc][mr][mc] = " "
        
        # Prefer center board and corners
        strategic_moves = []
        other_moves = []
        for br, bc, mr, mc in all_moves:
            if br == 1 and bc == 1:  # Center board
                strategic_moves.insert(0, (br, bc, mr, mc))
            elif (br, bc) in [(0, 0), (0, 2), (2, 0), (2, 2)]:  # Corner boards
                strategic_moves.append((br, bc, mr, mc))
            else:
                other_moves.append((br, bc, mr, mc))
        
        all_moves = strategic_moves + other_moves
        return all_moves[0] if all_moves else random.choice(all_moves)

    def format_mega_board(self):
        """Return a simple multi-line string representation of the mega board with spaces for empty tiles."""
        lines = []
        for mega_row in range(3):
            for inner_row in range(3):
                row_str = ""
                for mega_col in range(3):
                    for inner_col in range(3):
                        cell = self.board[mega_row][mega_col][inner_row][inner_col]
                        row_str += (cell if cell != ' ' else ' ') + " "
                    row_str += " | "
                lines.append(row_str)
            lines.append("-" * 35)
        return "\n".join(lines)

    def write_mega_game_result(self, winner_symbol, path='mega_game_results.txt'):
        """Write mega tictactoe game result to file with timestamp."""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            winner = "Draw" if winner_symbol is None else f"Winner: {winner_symbol} ({self.get_winner_name(winner_symbol)})"
            
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} - {winner}\n")
                f.write(f"{self.name1} ({self.symbol1}) vs {self.name2} ({self.symbol2})\n")
                f.write("\n")
                f.write(self.format_mega_board())
                f.write("\n")
                f.write("\n---\n\n")
            print(f"Mega game result written to {path}")
        except Exception as e:
            print(f"Error writing mega game result to {path}: {e}")


# Module provides the TicTacToe game logic class. Use a separate launcher
# (for example `run.py`) to start the program in console or GUI mode.
