import pygame
from ..constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_OFFSET_X, BOARD_OFFSET_Y,
    CELL_SIZE
)


class InputHandler:
    """Handles user input and interaction."""
    
    @staticmethod
    def get_cell_from_click(pos):
        """Convert mouse click position to board cell coordinates using current display size."""
        x, y = pos
        screen = pygame.display.get_surface()
        if screen is None:
            return None, None
        width, height = screen.get_size()
        board_offset_x = (width - 3 * CELL_SIZE) // 2
        board_offset_y = (height - 3 * CELL_SIZE) // 2
        if board_offset_x <= x <= board_offset_x + 3 * CELL_SIZE and \
           board_offset_y <= y <= board_offset_y + 3 * CELL_SIZE:
            col = (x - board_offset_x) // CELL_SIZE
            row = (y - board_offset_y) // CELL_SIZE
            return row, col
        return None, None

    @staticmethod
    def mark_cell(board, row, col, active_symbol, move_count):
        """Mark a cell with the active player's symbol.
        
        Returns:
            tuple: (success: bool, new_move_count: int)
        """
        if row is None or col is None:
            return False, move_count
        if board[row][col] != " ":
            return False, move_count
        board[row][col] = active_symbol
        return True, move_count + 1

    @staticmethod
    def handle_menu_input(event, play_rect, scores_rect, settings_rect=None, quit_rect=None):
        """Handle input on the main menu.

        Returns:
            str: 'play', 'scores', 'settings', 'quit', or None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                return 'play'
            if scores_rect.collidepoint(event.pos):
                return 'scores'
            if settings_rect is not None and settings_rect.collidepoint(event.pos):
                return 'settings'
            if quit_rect is not None and quit_rect.collidepoint(event.pos):
                return 'quit'
        return None

    @staticmethod
    def handle_file_view_input(event, back_rect):
        """Handle input on the file view screens (back or escape).

        Returns:
            bool: True if should return to menu
        """
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE]:
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back_rect.collidepoint(event.pos):
                return True
        return False

    @staticmethod
    def handle_settings_input(event, symbols_rect, game_type_rect, bot_rect, game_mode_rect, theme_rect, sound_rect, back_rect):
        """Handle clicks in the settings screen.

        Returns:
            str: one of 'symbols','game_type','bot','toggle_game_mode','theme','sound','back', or None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if symbols_rect.collidepoint(event.pos):
                return 'symbols'
            if game_type_rect.collidepoint(event.pos):
                return 'game_type'
            if bot_rect.collidepoint(event.pos):
                return 'bot'
            if game_mode_rect.collidepoint(event.pos):
                return 'toggle_game_mode'
            if theme_rect.collidepoint(event.pos):
                return 'theme'
            if sound_rect.collidepoint(event.pos):
                return 'sound'
            if back_rect.collidepoint(event.pos):
                return 'back'
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE]:
                return 'back'
        return None

    @staticmethod
    def handle_name_entry_input(event, rect1, rect2, p1, p2, active):
        """Handle input during name entry.

        Returns:
            tuple: (p1_text, p2_text, active_player, should_continue: bool, error_message or None)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Clicking a box clears it and sets focus
            if rect1.collidepoint(event.pos):
                active = 1
                p1 = ''
            elif rect2.collidepoint(event.pos):
                active = 2
                p2 = ''
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # If blank, fill with defaults; then validate uniqueness
                p1_trim = p1.strip() or 'Player 1'
                p2_trim = p2.strip() or 'Player 2'
                if p1_trim.lower() == p2_trim.lower():
                    return p1, p2, active, False, 'Names must be different.'
                return p1_trim, p2_trim, active, True, None
            elif event.key == pygame.K_TAB:
                active = 2 if active == 1 else 1
            elif event.key == pygame.K_BACKSPACE:
                if active == 1:
                    p1 = p1[:-1]
                else:
                    p2 = p2[:-1]
            else:
                char = event.unicode
                if char and ord(char) >= 32:
                    if active == 1:
                        p1 += char
                    else:
                        p2 += char
        
        return p1, p2, active, False, None

    @staticmethod
    def handle_symbols_input(event, rect1, rect2, s1, s2, active):
        """Handle input during symbol entry.

        Returns:
            tuple: (s1_text, s2_text, active_player, should_continue: bool, error_message or None)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect1.collidepoint(event.pos):
                active = 1
            elif rect2.collidepoint(event.pos):
                active = 2
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Validate symbols: must be single non-space characters and different
                if not s1 or not s2:
                    return s1, s2, active, False, 'Both symbols must be set.'
                if len(s1) != 1 or s1.isspace() or len(s2) != 1 or s2.isspace():
                    return s1, s2, active, False, 'Symbols must be single non-space characters.'
                if s1 == s2:
                    return s1, s2, active, False, 'Symbols must be different.'
                return s1, s2, active, True, None
            elif event.key == pygame.K_TAB:
                active = 2 if active == 1 else 1
            elif event.key == pygame.K_BACKSPACE:
                if active == 1:
                    s1 = s1[:-1]
                else:
                    s2 = s2[:-1]
            else:
                char = event.unicode
                if char and ord(char) >= 32:
                    # keep only a single character per symbol
                    if active == 1:
                        s1 = (s1 + char)[-1]
                    else:
                        s2 = (s2 + char)[-1]

        return s1, s2, active, False, None

    @staticmethod
    def handle_end_screen_input(event, play_again_rect, quit_rect):
        """Handle input on the end game screen.
        
        Returns:
            str: 'play_again', 'quit', or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                return 'play_again'
            elif event.key == pygame.K_q:
                return 'quit'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_again_rect.collidepoint(event.pos):
                return 'play_again'
            elif quit_rect.collidepoint(event.pos):
                return 'quit'
        
        return None

    @staticmethod
    def handle_highscores_input(event, back_rect):
        """Handle input on the highscores screen.
        
        Returns:
            bool: True if should return to menu
        """
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE]:
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back_rect.collidepoint(event.pos):
                return True
        
        return False

    @staticmethod
    def handle_bot_difficulty_input(event, easy_rect, med_rect, hard_rect, back_rect):
        """Handle input on the bot difficulty selection screen.
        
        Returns:
            str: 'easy', 'medium', 'hard', 'back', or None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if easy_rect.collidepoint(event.pos):
                return 'easy'
            if med_rect.collidepoint(event.pos):
                return 'medium'
            if hard_rect.collidepoint(event.pos):
                return 'hard'
            if back_rect.collidepoint(event.pos):
                return 'back'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'back'
        
        return None

    @staticmethod
    def get_mega_cell_from_click(pos, renderer):
        """Convert mouse click to (board_row, board_col, cell_row, cell_col) for mega tictactoe."""
        x, y = pos
        
        # Use renderer's scaled mega board dimensions
        small_board_size = 3 * renderer.mega_cell_size
        
        if renderer.mega_board_offset_x <= x <= renderer.mega_board_offset_x + 3 * small_board_size and \
           renderer.mega_board_offset_y <= y <= renderer.mega_board_offset_y + 3 * small_board_size:
            rel_x = x - renderer.mega_board_offset_x
            rel_y = y - renderer.mega_board_offset_y
            board_col = rel_x // small_board_size
            board_row = rel_y // small_board_size
            cell_col = (rel_x % small_board_size) // renderer.mega_cell_size
            cell_row = (rel_y % small_board_size) // renderer.mega_cell_size
            
            # Validate bounds
            if 0 <= board_row < 3 and 0 <= board_col < 3 and 0 <= cell_row < 3 and 0 <= cell_col < 3:
                return board_row, board_col, cell_row, cell_col
        
        return None, None, None, None

    @staticmethod
    def mark_mega_cell(small_boards, mega_board, board_row, board_col, cell_row, cell_col, active_symbol):
        """Mark a cell in mega tictactoe. Return success bool."""
        if board_row is None or board_col is None or cell_row is None or cell_col is None:
            return False
        if mega_board[board_row][board_col] != " ":
            return False
        if small_boards[board_row][board_col][cell_row][cell_col] != " ":
            return False
        small_boards[board_row][board_col][cell_row][cell_col] = active_symbol
        return True
