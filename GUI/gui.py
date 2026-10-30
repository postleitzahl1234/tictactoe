import pygame
import sys
import json
import os
from datetime import datetime, timedelta
from .main import TicTacToe, MegaTicTacToe
from .renderers import ScreenRenderer
from .handlers import InputHandler
from .constants import CELL_SIZE, THEMES
from .sfx import get_sfx_manager


class TicTacToeGUI(TicTacToe):
    """Main GUI class that orchestrates the game flow and rendering."""
    
    def __init__(self, name1, name2, symbol1, symbol2):
        super().__init__(name1, name2, symbol1, symbol2)
        pygame.init()
        self.renderer = ScreenRenderer()
        self.input_handler = InputHandler()
        self.game_over = False
        self.game_result = ""
        self.clock = pygame.time.Clock()
        self.button_cooldown = 0
        self.cooldown_threshold = 100  # 100ms debounce
        self.current_theme = 'forest'  # Track current theme
        self.bot_difficulty = 'medium'  # Track bot difficulty
        self.sfx_manager = get_sfx_manager()  # Initialize SFX manager

    def _should_handle_input(self):
        """Check if enough time has passed to avoid button spam."""
        if self.button_cooldown <= 0:
            return True
        self.button_cooldown -= self.clock.get_time()
        return False

    def _trigger_cooldown(self):
        """Trigger the button cooldown after handling input."""
        self.button_cooldown = self.cooldown_threshold

    def is_winning_gui(self):
        """Check if the current active player has won."""
        b = self.board
        winner_symbol = ""
        # rows and columns
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] and b[i][0] != " ":
                winner_symbol = b[i][0]
                break
            if b[0][i] == b[1][i] == b[2][i] and b[0][i] != " ":
                winner_symbol = b[0][i]
                break
        # diagonals
        if winner_symbol == "":
            if b[0][0] == b[1][1] == b[2][2] and b[0][0] != " ":
                winner_symbol = b[0][0]
            elif b[0][2] == b[1][1] == b[2][0] and b[0][2] != " ":
                winner_symbol = b[0][2]

        return winner_symbol != ""

    def play_single_game_gui(self):
        """Play a single game in GUI mode."""
        self.set_starting_position()
        self.game_over = False
        self.game_result = ""
        self.user_quit_game = False  # Track if user quit to menu
        
        # Start playing music when game begins (Mario soundtrack for bot games only)
        if self.game_mode == 'singleplayer':
            self.sfx_manager.play_background_music()
        
        self.renderer.clear_screen()
        self.renderer.draw_lines()
        self.renderer.draw_board(self.board, self.symbol1, self.symbol2)
        self.renderer.draw_player_status(
            self.current_player_name(), self.active_symbol, self.symbol1,
            False, "", self.name1, self.name2, self.win_counts
        )
        self.renderer.update_display()

        while not self.game_over and not self.user_quit_game:
            # If singleplayer and it's player 2's turn, let the bot play
            if self.game_mode == 'singleplayer' and self.active_player == 2 and not self.game_over:
                try:
                    pygame.time.wait(300)
                    res = self.get_bot_move(self.bot_difficulty)
                    if not res:
                        r, c = None, None
                    else:
                        r, c = res
                except Exception:
                    r, c = None, None
                if r is not None and c is not None:
                    # ensure the cell is free then mark
                    if self.board[r][c] == ' ':
                        self.board[r][c] = self.active_symbol
                        self.move_count += 1

                        self.renderer.clear_screen()
                        self.renderer.draw_lines()
                        self.renderer.draw_board(self.board, self.symbol1, self.symbol2)

                        if self.is_winning_gui():
                            self.register_win(self.active_symbol)
                            try:
                                self.write_game_result(self.active_symbol)
                            except Exception:
                                pass
                            self.game_over = True
                            self.game_result = f"{self.current_player_name()} ({self.active_symbol}) has won!"
                            # Play win sound if bot won (player lost)
                            if self.game_mode == 'singleplayer' and self.active_player == 2:
                                self.sfx_manager.play_lose_sound()
                        elif self.move_count >= 9:
                            self.game_over = True
                            self.game_result = "It's a draw!"
                            try:
                                self.write_game_result(None)
                            except Exception:
                                pass
                        else:
                            self.change_active_player()

                        self.renderer.draw_player_status(
                            self.current_player_name(), self.active_symbol, self.symbol1,
                            self.game_over, self.game_result, self.name1, self.name2, self.win_counts
                        )
                        self.renderer.update_display()
                        continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.user_quit_game = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = self.input_handler.get_cell_from_click(event.pos)
                    marked, self.move_count = self.input_handler.mark_cell(
                        self.board, row, col, self.active_symbol, self.move_count
                    )
                    
                    if marked:
                        self.renderer.clear_screen()
                        self.renderer.draw_lines()
                        self.renderer.draw_board(self.board, self.symbol1, self.symbol2)

                        if self.is_winning_gui():
                            # Register win and persist
                            self.register_win(self.active_symbol)
                            try:
                                self.write_game_result(self.active_symbol)
                            except Exception:
                                pass
                            self.game_over = True
                            self.game_result = f"{self.current_player_name()} ({self.active_symbol}) has won!"
                            # Play win sound if player won in bot game
                            if self.game_mode == 'singleplayer' and self.active_player == 1:
                                self.sfx_manager.play_win_sound()
                        elif self.move_count >= 9:
                            self.game_over = True
                            self.game_result = "It's a draw!"
                            try:
                                self.write_game_result(None)
                            except Exception:
                                pass
                        else:
                            self.change_active_player()

                        self.renderer.draw_player_status(
                            self.current_player_name(), self.active_symbol, self.symbol1,
                            self.game_over, self.game_result, self.name1, self.name2, self.win_counts
                        )
                        self.renderer.update_display()

        if not self.user_quit_game:
            play_again = self.draw_end_screen()
            return play_again
        return False

    def draw_end_screen(self):
        """Display the end game screen with play again and quit options."""
        pygame.time.wait(500)
        self.renderer.clear_screen()
        self.renderer.draw_mega_lines()
        self.renderer.draw_mega_board(self.board, self.claimed_boards, self.active_board)
        self.renderer.draw_player_status(self.current_player_name(), self.active_symbol, self.symbol1,
                                        True, self.game_result, self.name1, self.name2, self.win_counts)

        button_y = self.renderer.mega_board_offset_y + 3 * (3 * self.renderer.mega_cell_size) + 40
        btn_w, btn_h = 120, 50
        spacing = 30
        
        # Play Again button on the left
        play_again_rect = pygame.Rect(
            self.renderer.width // 2 - btn_w - spacing // 2,
            button_y,
            btn_w,
            btn_h
        )
        
        # Quit button on the right
        quit_rect = pygame.Rect(
            self.renderer.width // 2 + spacing // 2,
            button_y,
            btn_w,
            btn_h
        )
        
        mpos = pygame.mouse.get_pos()
        play_color = self.renderer.button_hover_color if play_again_rect.collidepoint(mpos) else self.renderer.button_color
        quit_color = self.renderer.button_hover_color if quit_rect.collidepoint(mpos) else self.renderer.button_color

        # Draw Play Again button
        pygame.draw.rect(self.renderer.screen, play_color, play_again_rect)
        pygame.draw.rect(self.renderer.screen, (255, 255, 255), play_again_rect, 3)
        play_again_text = self.renderer.font_tiny.render("Play Again (Y)", True, self.renderer.text_color)
        self.renderer.screen.blit(play_again_text, (play_again_rect.centerx - play_again_text.get_width() // 2,
                                                   play_again_rect.centery - play_again_text.get_height() // 2))
        
        # Draw Quit button
        pygame.draw.rect(self.renderer.screen, quit_color, quit_rect)
        pygame.draw.rect(self.renderer.screen, (255, 255, 255), quit_rect, 3)
        quit_text = self.renderer.font_tiny.render("Quit (Q)", True, self.renderer.text_color)
        self.renderer.screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2,
                                             quit_rect.centery - quit_text.get_height() // 2))
        
        self.renderer.update_display()

        # Wait for user response
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                choice = self.input_handler.handle_end_screen_input(event, play_again_rect, quit_rect)
                if choice == 'play_again':
                    return True
                elif choice == 'quit':
                    return False

        return False

    def show_highscores_screen(self):
        """Highscores menu: view Regular or Mega Games (last 10 days)."""
        self.button_cooldown = 0
        while True:
            regular_rect, mega_rect, back_rect = self.renderer.draw_highscores_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if regular_rect.collidepoint(event.pos):
                        self.show_last_games_screen()

                    elif mega_rect.collidepoint(event.pos):
                        self.show_mega_games_screen()

                    elif back_rect.collidepoint(event.pos):
                        return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    def show_last_games_screen(self):
        """Display last game boards from the last 10 days."""
        lines = []
        try:
            if os.path.exists('game_results.txt'):
                with open('game_results.txt', 'r', encoding='utf-8') as f:
                    content = f.read()
                    # split entries by separator '---'
                    parts = [p.strip() for p in content.split('---') if p.strip()]
                    cutoff = datetime.now() - timedelta(days=10)
                    for p in parts:
                        # first line contains timestamp like 'YYYY-MM-DD HH:MM:SS - ...'
                        first_line, *rest = p.splitlines()
                        ts_part = first_line.split(' - ')[0].strip()
                        try:
                            ts = datetime.fromisoformat(ts_part)
                        except Exception:
                            # skip entries we can't parse
                            continue
                        if ts >= cutoff:
                            lines.append(first_line)
                            for l in rest:
                                lines.append(l)
                            lines.append('')
        except Exception:
            # fallback to an empty view
            lines = ['No recent games found.']

        offset = 0
        while True:
            back_rect, total, max_lines = self.renderer.draw_file_view('Last Games (last 10 days)', lines, offset)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.input_handler.handle_file_view_input(event, back_rect):
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if offset + max_lines < total:
                            offset += max_lines
                    elif event.key == pygame.K_UP:
                        if offset - max_lines >= 0:
                            offset -= max_lines
            self.clock.tick(60)

    def show_mega_games_screen(self):
        """Display mega game boards from the last 10 days."""
        lines = []
        try:
            if os.path.exists('mega_game_results.txt'):
                with open('mega_game_results.txt', 'r', encoding='utf-8') as f:
                    content = f.read()
                    # split entries by separator '---'
                    parts = [p.strip() for p in content.split('---') if p.strip()]
                    cutoff = datetime.now() - timedelta(days=10)
                    for p in parts:
                        # first line contains timestamp like 'YYYY-MM-DD HH:MM:SS - ...'
                        first_line, *rest = p.splitlines()
                        ts_part = first_line.split(' - ')[0].strip()
                        try:
                            ts = datetime.fromisoformat(ts_part)
                        except Exception:
                            # skip entries we can't parse
                            continue
                        if ts >= cutoff:
                            lines.append(first_line)
                            for l in rest:
                                lines.append(l)
                            lines.append('')
        except Exception:
            # fallback to an empty view
            lines = ['No recent mega games found.']

        offset = 0
        while True:
            back_rect, total, max_lines = self.renderer.draw_file_view('Mega Games (last 10 days)', lines, offset)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.input_handler.handle_file_view_input(event, back_rect):
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if offset + max_lines < total:
                            offset += max_lines
                    elif event.key == pygame.K_UP:
                        if offset - max_lines >= 0:
                            offset -= max_lines
            self.clock.tick(60)

    def show_start_screen(self):
        """Display the start splash screen, skip with Space."""
        self.renderer.draw_start_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
            self.clock.tick(60)

    def show_main_menu(self):
        """Display the main menu and handle user choices."""
        play_rect, scores_rect, settings_rect, quit_rect = self.renderer.draw_main_menu()
        self.button_cooldown = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                
                if not self._should_handle_input():
                    continue
                    
                choice = self.input_handler.handle_menu_input(event, play_rect, scores_rect, settings_rect, quit_rect)
                if choice:
                    self._trigger_cooldown()
                    if choice == 'settings':
                        self.show_settings_menu()
                        # Check if game type was changed in settings
                        if hasattr(self, 'game_type_changed') and self.game_type_changed:
                            return 'game_type_changed'
                        play_rect, scores_rect, settings_rect, quit_rect = self.renderer.draw_main_menu()
                        self.button_cooldown = 0
                        break
                    elif choice == 'quit':
                        pygame.quit()
                        sys.exit()
                    return choice
            
            self.clock.tick(60)

    def show_name_entry(self):
        """Display the name entry screen."""
        p1 = self.name1
        p2 = self.name2
        active = 1
        err_msg = None

        clock = pygame.time.Clock()
        while True:
            res = self.renderer.draw_name_entry(p1, p2, active, err_msg)
            if not res:
                # nothing to draw; continue loop
                continue
            rect1, rect2 = res

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                p1, p2, active, should_continue, error = self.input_handler.handle_name_entry_input(
                    event, rect1, rect2, p1, p2, active
                )
                
                if error:
                    # pass error to renderer for display
                    err_msg = error
                else:
                    err_msg = None

                if should_continue:
                    # names are already trimmed by handler
                    self.set_player_names(p1, p2)
                    return

            clock.tick(30)

    def set_player_names(self, p1, p2):
        """Set player names, preserving existing win counts."""
        old = dict(self.win_counts)
        self.name1 = p1
        self.name2 = p2
        self.win_counts = {p1: old.get(p1, 0), p2: old.get(p2, 0)}

    def show_symbols_menu(self):
        """Display the symbols selection screen."""
        s1 = ''
        s2 = ''
        active = 1
        error = None
        self.button_cooldown = 0

        while True:
            res = self.renderer.draw_symbols_menu(s1, s2, active, error)
            if not res:
                continue
            rect1, rect2 = res

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                s1, s2, active, should_continue, error = self.input_handler.handle_symbols_input(
                    event, rect1, rect2, s1, s2, active
                )

                if should_continue:
                    self.set_player_symbols(s1, s2)
                    return

            self.clock.tick(60)

    def set_player_symbols(self, s1, s2):
        """Set player symbols and adjust active symbol if needed."""
        self.symbol1 = s1
        self.symbol2 = s2
        # ensure active symbol matches the active player
        self.active_symbol = self.symbol1 if self.active_player == 1 else self.symbol2

    def show_settings_menu(self):
        """Display the settings menu and handle actions."""
        self.button_cooldown = 0
        while True:
            game_type = getattr(self, 'game_type', 'regular')
            (symbols_rect, game_type_rect, bot_rect, game_mode_rect, theme_rect, sound_rect, back_rect) = self.renderer.draw_settings_menu(
                self.game_mode, getattr(self, 'bot_difficulty', None), game_type, self.sfx_manager.is_sound_enabled()
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not self._should_handle_input():
                    continue

                action = self.input_handler.handle_settings_input(
                    event, symbols_rect, game_type_rect, bot_rect, game_mode_rect, theme_rect, sound_rect, back_rect
                )

                if action:
                    self._trigger_cooldown()

                if action == 'symbols':
                    self.show_symbols_menu()
                    self.button_cooldown = 0
                    break
                elif action == 'game_type':
                    # Toggle between regular and mega
                    new_type = 'mega' if game_type == 'regular' else 'regular'
                    self.game_type = new_type
                    self.new_game_type = new_type
                    self.game_type_changed = True
                    return
                elif action == 'bot':
                    # Cycle through difficulty levels
                    difficulty_order = ['easy', 'medium', 'hard']
                    current_idx = difficulty_order.index(self.bot_difficulty)
                    new_idx = (current_idx + 1) % len(difficulty_order)
                    self.bot_difficulty = difficulty_order[new_idx]
                    self.button_cooldown = 0
                    break
                elif action == 'toggle_game_mode':
                    new_mode = 'singleplayer' if self.game_mode == 'multiplayer' else 'multiplayer'
                    self.set_game_mode(new_mode)
                    # ensure a bot exists when switching to singleplayer
                    if new_mode == 'singleplayer' and not hasattr(self, 'bot_difficulty'):
                        self.bot_difficulty = 'medium'
                        # set computer as player 2
                        self.name2 = 'Computer'
                    self.button_cooldown = 0
                    break
                elif action == 'theme':
                    # Cycle through theme options
                    theme_order = ['forest', 'soft desert', 'misty pastel', 'ocean breeze']
                    current_idx = theme_order.index(self.current_theme)
                    new_idx = (current_idx + 1) % len(theme_order)
                    self.current_theme = theme_order[new_idx]
                    self.renderer.set_theme(self.current_theme)
                    self.button_cooldown = 0
                    break
                elif action == 'sound':
                    # Toggle sound on/off
                    self.sfx_manager.toggle_sound()
                    self.button_cooldown = 0
                    break
                elif action == 'back':
                    return

            self.clock.tick(60)



    def set_game_mode(self, mode):
        """Set the game mode: 'multiplayer' or 'singleplayer'."""
        if mode not in ('multiplayer', 'singleplayer'):
            return
        self.game_mode = mode

    def game_loop_gui(self):
        """Main game loop - show menu and handle user choices."""
        while True:
            choice = self.show_main_menu()
            if choice == 'play':
                play_again = True
                while play_again:
                    play_again = self.play_single_game_gui()
            elif choice == 'scores':
                self.show_highscores_screen()
            elif choice == 'game_type_changed':
                # Game type was changed in settings, exit to restart
                return
            else:
                pygame.quit()
                sys.exit()


class MegaTicTacToeGUI(MegaTicTacToe):
    """GUI for Mega Tic Tac Toe."""
    
    def __init__(self, name1, name2, symbol1, symbol2):
        super().__init__(name1, name2, symbol1, symbol2)
        pygame.init()
        self.renderer = ScreenRenderer()
        self.input_handler = InputHandler()
        self.game_over = False
        self.game_result = ""
        self.clock = pygame.time.Clock()
        self.button_cooldown = 0
        self.cooldown_threshold = 100
        self.current_theme = 'forest'  # Track current theme
        self.bot_difficulty = 'medium'  # Track bot difficulty
        self.sfx_manager = get_sfx_manager()  # Initialize SFX manager

    def write_game_result(self, winner_symbol, path='game_results.txt'):
        """Override to save mega game results to separate file."""
        self.write_mega_game_result(winner_symbol, 'mega_game_results.txt')

    def _should_handle_input(self):
        """Check if enough time has passed to avoid button spam."""
        if self.button_cooldown <= 0:
            return True
        self.button_cooldown -= self.clock.get_time()
        return False

    def _trigger_cooldown(self):
        """Trigger the button cooldown after handling input."""
        self.button_cooldown = self.cooldown_threshold

    def play_single_game_gui(self):
        """Play a single mega tictactoe game in GUI mode."""
        self.set_starting_position()
        self.game_over = False
        self.game_result = ""
        self.user_quit_game = False  # Track if user quit to menu
        
        # Start playing music when game begins (Mario soundtrack for bot games only)
        if self.game_mode == 'singleplayer':
            self.sfx_manager.play_background_music()
        else:
            self.sfx_manager.play_music()
        
        self.renderer.clear_screen()
        self.renderer.draw_mega_lines()
        self.renderer.draw_mega_board(self.board, self.claimed_boards, self.active_board)
        self.renderer.draw_player_status(
            self.current_player_name(), self.active_symbol, self.symbol1,
            False, "", self.name1, self.name2, self.win_counts
        )
        self.renderer.update_display()

        while not self.game_over and not self.user_quit_game:
            # If singleplayer and it's player 2's turn, let the bot play
            if self.game_mode == 'singleplayer' and self.active_player == 2 and not self.game_over:
                try:
                    pygame.time.wait(200)
                    res = self.get_bot_move_mega(self.bot_difficulty)
                    if not res:
                        br, bc, mr, mc = None, None, None, None
                    else:
                        br, bc, mr, mc = res
                except Exception:
                    br, bc, mr, mc = None, None, None, None
                
                if br is not None and bc is not None and mr is not None and mc is not None:
                    # Try to make the move
                    if self.play_move_in_board(br, bc, mr, mc):
                        self.renderer.clear_screen()
                        self.renderer.draw_mega_lines()
                        self.renderer.draw_mega_board(self.board, self.claimed_boards, self.active_board)

                        mega_winner = self.check_mega_winner()
                        if mega_winner is not None and mega_winner != "D":
                            self.register_win(mega_winner)
                            try:
                                self.write_game_result(mega_winner)
                            except Exception:
                                pass
                            self.game_over = True
                            self.game_result = f"{self.current_player_name()} ({self.active_symbol}) has won!"
                            # Play lose sound if bot won (player lost)
                            if self.game_mode == 'singleplayer' and self.active_player == 2:
                                self.sfx_manager.play_lose_sound()
                        elif mega_winner == "D":
                            self.game_over = True
                            self.game_result = "It's a draw!"
                            try:
                                self.write_game_result(None)
                            except Exception:
                                pass
                        else:
                            self.change_active_player()

                        self.renderer.draw_player_status(
                            self.current_player_name(), self.active_symbol, self.symbol1,
                            self.game_over, self.game_result, self.name1, self.name2, self.win_counts
                        )
                        self.renderer.update_display()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.user_quit_game = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    br, bc, mr, mc = self.input_handler.get_mega_cell_from_click(event.pos, self.renderer)
                    marked = self.play_move_in_board(br, bc, mr, mc) if br is not None else False
                    
                    if marked:
                        self.renderer.clear_screen()
                        self.renderer.draw_mega_lines()
                        self.renderer.draw_mega_board(self.board, self.claimed_boards, self.active_board)

                        mega_winner = self.check_mega_winner()
                        if mega_winner is not None and mega_winner != "D":
                            self.register_win(mega_winner)
                            try:
                                self.write_game_result(mega_winner)
                            except Exception:
                                pass
                            self.game_over = True
                            self.game_result = f"{self.current_player_name()} ({self.active_symbol}) has won!"
                            # Play win sound if player won in bot game
                            if self.game_mode == 'singleplayer' and self.active_player == 1:
                                self.sfx_manager.play_win_sound()
                        elif mega_winner == "D":
                            self.game_over = True
                            self.game_result = "It's a draw!"
                            try:
                                self.write_game_result(None)
                            except Exception:
                                pass
                        else:
                            self.change_active_player()

                        self.renderer.draw_player_status(
                            self.current_player_name(), self.active_symbol, self.symbol1,
                            self.game_over, self.game_result, self.name1, self.name2, self.win_counts
                        )
                        self.renderer.update_display()
            
            self.clock.tick(60)

        if not self.user_quit_game:
            self.draw_end_screen()
        return not self.user_quit_game

    def draw_end_screen(self):
        """Display the end game screen with play again and quit options."""
        pygame.time.wait(500)
        self.renderer.clear_screen()
        self.renderer.draw_mega_lines()
        self.renderer.draw_mega_board(self.board, self.claimed_boards, self.active_board)
        self.renderer.draw_player_status(self.current_player_name(), self.active_symbol, self.symbol1,
                                        True, self.game_result, self.name1, self.name2, self.win_counts)

        button_y = self.renderer.mega_board_offset_y + 3 * (3 * self.renderer.mega_cell_size) + 40
        btn_w, btn_h = 120, 50
        spacing = 30
        
        # Play Again button on the left
        play_again_rect = pygame.Rect(
            self.renderer.width // 2 - btn_w - spacing // 2,
            button_y,
            btn_w,
            btn_h
        )
        
        # Quit button on the right
        quit_rect = pygame.Rect(
            self.renderer.width // 2 + spacing // 2,
            button_y,
            btn_w,
            btn_h
        )
        
        mpos = pygame.mouse.get_pos()
        play_color = self.renderer.button_hover_color if play_again_rect.collidepoint(mpos) else self.renderer.button_color
        quit_color = self.renderer.button_hover_color if quit_rect.collidepoint(mpos) else self.renderer.button_color

        # Draw Play Again button
        pygame.draw.rect(self.renderer.screen, play_color, play_again_rect)
        pygame.draw.rect(self.renderer.screen, (255, 255, 255), play_again_rect, 3)
        play_again_text = self.renderer.font_tiny.render("Play Again (Y)", True, self.renderer.text_color)
        self.renderer.screen.blit(play_again_text, (play_again_rect.centerx - play_again_text.get_width() // 2,
                                                   play_again_rect.centery - play_again_text.get_height() // 2))
        
        # Draw Quit button
        pygame.draw.rect(self.renderer.screen, quit_color, quit_rect)
        pygame.draw.rect(self.renderer.screen, (255, 255, 255), quit_rect, 3)
        quit_text = self.renderer.font_tiny.render("Quit (Q)", True, self.renderer.text_color)
        self.renderer.screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2,
                                             quit_rect.centery - quit_text.get_height() // 2))
        
        self.renderer.update_display()

        # Wait for user response
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                choice = self.input_handler.handle_end_screen_input(event, play_again_rect, quit_rect)
                if choice == 'play_again':
                    return True
                elif choice == 'quit':
                    return False

        return False

    def show_main_menu(self):
        """Display the main menu and handle user choices."""
        play_rect, scores_rect, settings_rect, quit_rect = self.renderer.draw_main_menu()
        self.button_cooldown = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                
                if not self._should_handle_input():
                    continue
                    
                choice = self.input_handler.handle_menu_input(event, play_rect, scores_rect, settings_rect, quit_rect)
                if choice:
                    self._trigger_cooldown()
                    if choice == 'settings':
                        self.show_settings_menu()
                        # Check if game type was changed in settings
                        if hasattr(self, 'game_type_changed') and self.game_type_changed:
                            return 'game_type_changed'
                        play_rect, scores_rect, settings_rect, quit_rect = self.renderer.draw_main_menu()
                        self.button_cooldown = 0
                        break
                    elif choice == 'quit':
                        pygame.quit()
                        sys.exit()
                    return choice
            
            self.clock.tick(60)

    def show_settings_menu(self):
        """Display the settings menu and handle actions."""
        self.button_cooldown = 0
        while True:
            game_type = getattr(self, 'game_type', 'mega')
            (symbols_rect, game_type_rect, bot_rect, game_mode_rect, theme_rect, sound_rect, back_rect) = self.renderer.draw_settings_menu(
                self.game_mode, getattr(self, 'bot_difficulty', None), game_type, self.sfx_manager.is_sound_enabled()
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not self._should_handle_input():
                    continue

                action = self.input_handler.handle_settings_input(
                    event, symbols_rect, game_type_rect, bot_rect, game_mode_rect, theme_rect, sound_rect, back_rect
                )

                if action:
                    self._trigger_cooldown()

                if action == 'symbols':
                    self.show_symbols_menu()
                    self.button_cooldown = 0
                    break
                elif action == 'game_type':
                    # Toggle between regular and mega
                    new_type = 'mega' if game_type == 'regular' else 'regular'
                    self.game_type = new_type
                    self.new_game_type = new_type
                    self.game_type_changed = True
                    return
                elif action == 'bot':
                    # Cycle through difficulty levels
                    difficulty_order = ['easy', 'medium', 'hard']
                    current_idx = difficulty_order.index(self.bot_difficulty)
                    new_idx = (current_idx + 1) % len(difficulty_order)
                    self.bot_difficulty = difficulty_order[new_idx]
                    self.button_cooldown = 0
                    break
                elif action == 'toggle_game_mode':
                    new_mode = 'singleplayer' if self.game_mode == 'multiplayer' else 'multiplayer'
                    self.set_game_mode(new_mode)
                    if new_mode == 'singleplayer' and not hasattr(self, 'bot_difficulty'):
                        self.bot_difficulty = 'medium'
                        self.name2 = 'Computer'
                    self.button_cooldown = 0
                    break
                elif action == 'theme':
                    # Cycle through theme options
                    theme_order = ['forest', 'soft desert', 'misty pastel', 'ocean breeze']
                    current_idx = theme_order.index(self.current_theme)
                    new_idx = (current_idx + 1) % len(theme_order)
                    self.current_theme = theme_order[new_idx]
                    self.renderer.set_theme(self.current_theme)
                    self.button_cooldown = 0
                    break
                elif action == 'sound':
                    # Toggle sound on/off
                    self.sfx_manager.toggle_sound()
                    self.button_cooldown = 0
                    break
                elif action == 'back':
                    return

            self.clock.tick(60)

    def show_symbols_menu(self):
        """Display the symbols selection screen."""
        s1 = ''
        s2 = ''
        active = 1
        error = None
        self.button_cooldown = 0

        while True:
            res = self.renderer.draw_symbols_menu(s1, s2, active, error)
            if not res:
                continue
            rect1, rect2 = res

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                s1, s2, active, should_continue, error = self.input_handler.handle_symbols_input(
                    event, rect1, rect2, s1, s2, active
                )

                if should_continue:
                    self.set_player_symbols(s1, s2)
                    return

            self.clock.tick(60)

    def set_player_symbols(self, s1, s2):
        """Set player symbols and adjust active symbol if needed."""
        self.symbol1 = s1
        self.symbol2 = s2
        self.active_symbol = self.symbol1 if self.active_player == 1 else self.symbol2

    def show_highscores_screen(self):
        """Highscores menu: view Regular or Mega Games (last 10 days)."""
        self.button_cooldown = 0
        while True:
            regular_rect, mega_rect, back_rect = self.renderer.draw_highscores_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if regular_rect.collidepoint(event.pos):
                        self.show_last_games_screen()

                    elif mega_rect.collidepoint(event.pos):
                        self.show_mega_games_screen()

                    elif back_rect.collidepoint(event.pos):
                        return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    def show_last_games_screen(self):
        """Display last game boards from the last 10 days."""
        lines = []
        try:
            if os.path.exists('game_results.txt'):
                with open('game_results.txt', 'r', encoding='utf-8') as f:
                    content = f.read()
                    parts = [p.strip() for p in content.split('---') if p.strip()]
                    cutoff = datetime.now() - timedelta(days=10)
                    for p in parts:
                        first_line, *rest = p.splitlines()
                        ts_part = first_line.split(' - ')[0].strip()
                        try:
                            ts = datetime.fromisoformat(ts_part)
                        except Exception:
                            continue
                        if ts >= cutoff:
                            lines.append(first_line)
                            for l in rest:
                                lines.append(l)
                            lines.append('')
        except Exception:
            lines = ['No recent games found.']

        offset = 0
        while True:
            back_rect, total, max_lines = self.renderer.draw_file_view('Last Games (last 10 days)', lines, offset)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.input_handler.handle_file_view_input(event, back_rect):
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if offset + max_lines < total:
                            offset += max_lines
                    elif event.key == pygame.K_UP:
                        if offset - max_lines >= 0:
                            offset -= max_lines
            self.clock.tick(60)

    def show_mega_games_screen(self):
        """Display mega game boards from the last 10 days."""
        lines = []
        try:
            if os.path.exists('mega_game_results.txt'):
                with open('mega_game_results.txt', 'r', encoding='utf-8') as f:
                    content = f.read()
                    parts = [p.strip() for p in content.split('---') if p.strip()]
                    cutoff = datetime.now() - timedelta(days=10)
                    for p in parts:
                        first_line, *rest = p.splitlines()
                        ts_part = first_line.split(' - ')[0].strip()
                        try:
                            ts = datetime.fromisoformat(ts_part)
                        except Exception:
                            continue
                        if ts >= cutoff:
                            lines.append(first_line)
                            for l in rest:
                                lines.append(l)
                            lines.append('')
        except Exception:
            lines = ['No recent mega games found.']

        offset = 0
        while True:
            back_rect, total, max_lines = self.renderer.draw_file_view('Mega Games (last 10 days)', lines, offset)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.input_handler.handle_file_view_input(event, back_rect):
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if offset + max_lines < total:
                            offset += max_lines
                    elif event.key == pygame.K_UP:
                        if offset - max_lines >= 0:
                            offset -= max_lines
            self.clock.tick(60)

    def set_game_mode(self, mode):
        """Set the game mode: 'multiplayer' or 'singleplayer'."""
        if mode not in ('multiplayer', 'singleplayer'):
            return
        self.game_mode = mode

    def game_loop_gui(self):
        """Main game loop - show menu and handle user choices."""
        while True:
            choice = self.show_main_menu()
            if choice == 'play':
                play_again = True
                while play_again:
                    play_again = self.play_single_game_gui()
            elif choice == 'scores':
                self.show_highscores_screen()
            elif choice == 'game_type_changed':
                # Game type was changed in settings, exit to restart
                return
            else:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    # Start GUI (name-entry removed in v2.2)
    game = TicTacToeGUI("Player 1", "Player 2", "O", "X")
    game.game_loop_gui()
