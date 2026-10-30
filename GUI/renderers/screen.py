import pygame
from ..constants import (
    CELL_SIZE, LINE_WIDTH, CIRCLE_RADIUS, CIRCLE_WIDTH,
    CROSS_WIDTH, SPACE, FONT_LARGE, FONT_SMALL, FONT_TINY,
    BOARD_WIDTH, BOARD_HEIGHT, THEMES, DEFAULT_THEME
)


class ScreenRenderer:
    """Handles all screen rendering and drawing operations (fullscreen aware)."""
    
    def __init__(self, theme='forest'):
        """Initialize the pygame screen (fullscreen) and fonts."""
        # Start fullscreen so the game covers the entire display
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Tic-Tac-Toe v2.3')
        self.width, self.height = self.screen.get_size()
        # board offsets computed dynamically so board stays centered on any resolution
        self.board_offset_x = (self.width - BOARD_WIDTH) // 2
        self.board_offset_y = (self.height - BOARD_HEIGHT) // 2

        # Calculate scaled cell size for mega tictactoe (fit 9x9 grid on screen)
        margin = 100
        available_width = self.width - (2 * margin)
        available_height = self.height - (2 * margin) - 100  # Extra space for status
        self.mega_cell_size = min(available_width, available_height) // 9
        self.mega_cell_size = max(30, self.mega_cell_size)  # Minimum cell size
        
        # Mega board dimensions
        self.mega_board_width = 9 * self.mega_cell_size
        self.mega_board_height = 9 * self.mega_cell_size
        self.mega_board_offset_x = (self.width - self.mega_board_width) // 2
        self.mega_board_offset_y = (self.height - self.mega_board_height) // 2 - 30

        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        self.font_tiny = pygame.font.Font(None, FONT_TINY)

        # Set theme
        self.set_theme(theme)

    def set_theme(self, theme_name):
        """Set the current theme colors."""
        if theme_name not in THEMES:
            theme_name = DEFAULT_THEME
        theme = THEMES[theme_name]
        self.text_color = theme['text']
        self.button_color = theme['button']
        self.button_hover_color = theme['button_hover']
        self.bg_color = theme['bg']
        self.circle_color = theme['circle']
        self.cross_color = theme['cross']
        self.line_color = theme['line']
        self.current_theme = theme_name

    def needs_black_button_border(self):
        """Check if current theme needs black button borders."""
        return self.current_theme in ('soft desert', 'ocean breeze')

    def draw_settings_menu(self, game_mode, bot_difficulty=None, game_type='regular', sound_enabled=True):
        """Draw the settings screen and return button rectangles.

        Buttons: Symbols, Bot Difficulty, Game Type, Game Mode, Theme, Sound, Back
        """
        self.clear_screen()
        title = self.font_large.render('Settings', True, self.text_color)
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)

        y_start = 140
        btn_w, btn_h = 360, 60
        gap = 20
        x = self.width // 2 - btn_w // 2

        symbols_rect = pygame.Rect(x, y_start, btn_w, btn_h)
        game_type_rect = pygame.Rect(x, y_start + (btn_h + gap), btn_w, btn_h)
        bot_rect = pygame.Rect(x, y_start + 2 * (btn_h + gap), btn_w, btn_h)
        game_mode_rect = pygame.Rect(x, y_start + 3 * (btn_h + gap), btn_w, btn_h)
        theme_rect = pygame.Rect(x, y_start + 4 * (btn_h + gap), btn_w, btn_h)
        sound_rect = pygame.Rect(x, y_start + 5 * (btn_h + gap), btn_w, btn_h)
        back_rect = pygame.Rect(self.width // 2 - 75, self.height - 120, 150, 50)

        mpos = pygame.mouse.get_pos()
        needs_black_border = self.needs_black_button_border()
        
        # Draw the buttons: Symbols, Game Type, Bot Difficulty
        for r, label in ((symbols_rect, 'Symbols'), (game_type_rect, f'Game Type: {game_type.capitalize()}')):
            color = self.button_hover_color if r.collidepoint(mpos) else self.button_color
            pygame.draw.rect(self.screen, color, r)
            pygame.draw.rect(self.screen, (255, 255, 255), r, 3)
            if needs_black_border:
                pygame.draw.rect(self.screen, (0, 0, 0), r, 2)
            text = self.font_small.render(label, True, self.text_color)
            self.screen.blit(text, (r.centerx - text.get_width() // 2, r.centery - text.get_height() // 2))

        # Bot difficulty button
        bot_color = self.button_hover_color if bot_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, bot_color, bot_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), bot_rect, 3)
        if needs_black_border:
            pygame.draw.rect(self.screen, (0, 0, 0), bot_rect, 2)
        bot_text = self.font_small.render(f'Bot Difficulty: {bot_difficulty or "-"}', True, self.text_color)
        self.screen.blit(bot_text, (bot_rect.centerx - bot_text.get_width() // 2, bot_rect.centery - bot_text.get_height() // 2))

        # Toggle game mode button (multiplayer/singleplayer)
        gm_color = self.button_hover_color if game_mode_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, gm_color, game_mode_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), game_mode_rect, 3)
        if needs_black_border:
            pygame.draw.rect(self.screen, (0, 0, 0), game_mode_rect, 2)
        gm_text = self.font_small.render(f'Game Mode: {game_mode}', True, self.text_color)
        self.screen.blit(gm_text, (game_mode_rect.centerx - gm_text.get_width() // 2, game_mode_rect.centery - gm_text.get_height() // 2))

        # Theme selector button
        theme_color = self.button_hover_color if theme_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, theme_color, theme_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), theme_rect, 3)
        if needs_black_border:
            pygame.draw.rect(self.screen, (0, 0, 0), theme_rect, 2)
        theme_text = self.font_small.render(f'Theme: {self.current_theme.title()}', True, self.text_color)
        self.screen.blit(theme_text, (theme_rect.centerx - theme_text.get_width() // 2, theme_rect.centery - theme_text.get_height() // 2))

        # Sound toggle button
        sound_status = 'ON' if sound_enabled else 'OFF'
        sound_color = self.button_hover_color if sound_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, sound_color, sound_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), sound_rect, 3)
        if needs_black_border:
            pygame.draw.rect(self.screen, (0, 0, 0), sound_rect, 2)
        sound_text = self.font_small.render(f'Sound: {sound_status}', True, self.text_color)
        self.screen.blit(sound_text, (sound_rect.centerx - sound_text.get_width() // 2, sound_rect.centery - sound_text.get_height() // 2))

        # Back button
        back_color = self.button_hover_color if back_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, back_color, back_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 3)
        if needs_black_border:
            pygame.draw.rect(self.screen, (0, 0, 0), back_rect, 2)
        back_text = self.font_tiny.render('Back', True, self.text_color)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))

        self.update_display()
        return symbols_rect, game_type_rect, bot_rect, game_mode_rect, theme_rect, sound_rect, back_rect

    def clear_screen(self):
        """Fill the screen with the background color."""
        self.screen.fill(self.bg_color)

    def update_display(self):
        """Update the pygame display."""
        pygame.display.update()

    def draw_lines(self):
        """Draw the tic-tac-toe grid lines centered on screen."""
        # Horizontal lines
        pygame.draw.line(self.screen, self.line_color,
                        (self.board_offset_x, self.board_offset_y + CELL_SIZE),
                        (self.board_offset_x + 3 * CELL_SIZE, self.board_offset_y + CELL_SIZE),
                        LINE_WIDTH)
        pygame.draw.line(self.screen, self.line_color,
                        (self.board_offset_x, self.board_offset_y + 2 * CELL_SIZE),
                        (self.board_offset_x + 3 * CELL_SIZE, self.board_offset_y + 2 * CELL_SIZE),
                        LINE_WIDTH)
        # Vertical lines
        pygame.draw.line(self.screen, self.line_color,
                        (self.board_offset_x + CELL_SIZE, self.board_offset_y),
                        (self.board_offset_x + CELL_SIZE, self.board_offset_y + 3 * CELL_SIZE),
                        LINE_WIDTH)
        pygame.draw.line(self.screen, self.line_color,
                        (self.board_offset_x + 2 * CELL_SIZE, self.board_offset_y),
                        (self.board_offset_x + 2 * CELL_SIZE, self.board_offset_y + 3 * CELL_SIZE),
                        LINE_WIDTH)
        # Draw border rectangle around grid with line_width thickness
        self.draw_grid_border(BOARD_WIDTH, BOARD_HEIGHT, self.board_offset_x, self.board_offset_y, LINE_WIDTH)

    def draw_grid_border(self, grid_width, grid_height, offset_x, offset_y, thickness):
        """Draw a rectangular border around a grid with specified thickness."""
        border_rect = pygame.Rect(offset_x, offset_y, grid_width, grid_height)
        pygame.draw.rect(self.screen, self.line_color, border_rect, thickness)

    def draw_button(self, rect, text, is_hovered):
        """Draw a button with hover effect."""
        color = self.button_hover_color if is_hovered else self.button_color
        pygame.draw.rect(self.screen, color, rect)
        text_surface = self.font_small.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_board_cell(self, row, col, symbol):
        """Draw a single cell on the board."""
        x = self.board_offset_x + col * CELL_SIZE + CELL_SIZE // 2
        y = self.board_offset_y + row * CELL_SIZE + CELL_SIZE // 2
        if symbol == 'O':
            pygame.draw.circle(self.screen, self.circle_color, (x, y), CIRCLE_RADIUS, CIRCLE_WIDTH)
        elif symbol == 'X':
            x1 = x - CELL_SIZE // 3
            y1 = y - CELL_SIZE // 3
            x2 = x + CELL_SIZE // 3
            y2 = y + CELL_SIZE // 3
            pygame.draw.line(self.screen, self.cross_color, (x1, y1), (x2, y2), CROSS_WIDTH)
            pygame.draw.line(self.screen, self.cross_color, (x1, y2), (x2, y1), CROSS_WIDTH)

    def draw_mega_board_cell(self, mega_row, mega_col, row=None, col=None, symbol=None):
        """Draw a cell or overlay on the mega board."""
        small_board_size = 3 * self.mega_cell_size
        base_x = self.mega_board_offset_x + mega_col * small_board_size
        base_y = self.mega_board_offset_y + mega_row * small_board_size

        if row is not None and col is not None:
            # Draw a specific cell
            x = base_x + col * self.mega_cell_size + self.mega_cell_size // 2
            y = base_y + row * self.mega_cell_size + self.mega_cell_size // 2
            if symbol == 'O':
                radius = max(4, self.mega_cell_size // 6)
                width = max(1, self.mega_cell_size // 20)
                pygame.draw.circle(self.screen, self.circle_color, (x, y), radius, width)
            elif symbol == 'X':
                space = max(3, self.mega_cell_size // 6)
                width = max(1, self.mega_cell_size // 20)
                x1 = x - self.mega_cell_size // 3
                y1 = y - self.mega_cell_size // 3
                x2 = x + self.mega_cell_size // 3
                y2 = y + self.mega_cell_size // 3
                pygame.draw.line(self.screen, self.cross_color, (x1, y1), (x2, y2), width)
                pygame.draw.line(self.screen, self.cross_color, (x1, y2), (x2, y1), width)
        else:
            # Draw a large semi-transparent overlay on a won small board
            overlay_color = self.circle_color if symbol == "O" else self.cross_color
            overlay = pygame.Surface((small_board_size, small_board_size))
            overlay.set_alpha(60)
            overlay.fill(overlay_color)
            self.screen.blit(overlay, (base_x, base_y))

    def draw_board(self, board, symbol1, symbol2):
        """Draw the current board state."""
        for row in range(3):
            for col in range(3):
                if board[row][col] == symbol1:
                    self.draw_circle(row, col)
                elif board[row][col] == symbol2:
                    self.draw_cross(row, col)

    def draw_circle(self, row, col):
        """Draw a circle at the specified board position."""
        x = self.board_offset_x + col * CELL_SIZE + CELL_SIZE // 2
        y = self.board_offset_y + row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(self.screen, self.circle_color, (x, y), CIRCLE_RADIUS, CIRCLE_WIDTH)

    def draw_cross(self, row, col):
        """Draw a cross at the specified board position."""
        x1 = self.board_offset_x + col * CELL_SIZE + SPACE
        y1 = self.board_offset_y + row * CELL_SIZE + CELL_SIZE - SPACE
        x2 = self.board_offset_x + col * CELL_SIZE + CELL_SIZE - SPACE
        y2 = self.board_offset_y + row * CELL_SIZE + SPACE
        pygame.draw.line(self.screen, self.cross_color, (x1, y1), (x2, y2), CROSS_WIDTH)

        x1 = self.board_offset_x + col * CELL_SIZE + SPACE
        y1 = self.board_offset_y + row * CELL_SIZE + SPACE
        x2 = self.board_offset_x + col * CELL_SIZE + CELL_SIZE - SPACE
        y2 = self.board_offset_y + row * CELL_SIZE + CELL_SIZE - SPACE
        pygame.draw.line(self.screen, self.cross_color, (x1, y1), (x2, y2), CROSS_WIDTH)

    def draw_mega_lines(self):
        """Draw the mega tic-tac-toe grid (3x3 of small boards with larger separators)."""
        small_board_size = 3 * self.mega_cell_size
        # Draw the 3x3 mega grid with thicker lines
        mega_line_width = max(4, self.mega_cell_size // 8)
        
        # Horizontal lines (between mega rows)
        pygame.draw.line(self.screen, self.line_color,
                        (self.mega_board_offset_x, self.mega_board_offset_y + small_board_size),
                        (self.mega_board_offset_x + 3 * small_board_size, self.mega_board_offset_y + small_board_size),
                        mega_line_width)
        pygame.draw.line(self.screen, self.line_color,
                        (self.mega_board_offset_x, self.mega_board_offset_y + 2 * small_board_size),
                        (self.mega_board_offset_x + 3 * small_board_size, self.mega_board_offset_y + 2 * small_board_size),
                        mega_line_width)
        
        # Vertical lines (between mega columns)
        pygame.draw.line(self.screen, self.line_color,
                        (self.mega_board_offset_x + small_board_size, self.mega_board_offset_y),
                        (self.mega_board_offset_x + small_board_size, self.mega_board_offset_y + 3 * small_board_size),
                        mega_line_width)
        pygame.draw.line(self.screen, self.line_color,
                        (self.mega_board_offset_x + 2 * small_board_size, self.mega_board_offset_y),
                        (self.mega_board_offset_x + 2 * small_board_size, self.mega_board_offset_y + 3 * small_board_size),
                        mega_line_width)
        
        # Draw small grid lines within each board
        for mega_row in range(3):
            for mega_col in range(3):
                base_x = self.mega_board_offset_x + mega_col * small_board_size
                base_y = self.mega_board_offset_y + mega_row * small_board_size
                
                # Horizontal lines within board
                line_width = max(1, self.mega_cell_size // 16)
                pygame.draw.line(self.screen, self.line_color,
                                (base_x, base_y + self.mega_cell_size),
                                (base_x + small_board_size, base_y + self.mega_cell_size),
                                line_width)
                pygame.draw.line(self.screen, self.line_color,
                                (base_x, base_y + 2 * self.mega_cell_size),
                                (base_x + small_board_size, base_y + 2 * self.mega_cell_size),
                                line_width)
                
                # Vertical lines within board
                pygame.draw.line(self.screen, self.line_color,
                                (base_x + self.mega_cell_size, base_y),
                                (base_x + self.mega_cell_size, base_y + small_board_size),
                                line_width)
                pygame.draw.line(self.screen, self.line_color,
                                (base_x + 2 * self.mega_cell_size, base_y),
                                (base_x + 2 * self.mega_cell_size, base_y + small_board_size),
                                line_width)
        
        # Draw border rectangle around mega grid with mega_line_width thickness
        self.draw_grid_border(self.mega_board_width, self.mega_board_height, 
                             self.mega_board_offset_x, self.mega_board_offset_y, mega_line_width)

    def draw_mega_board(self, board, claimed_boards, active_board=None):
        """Draw the mega board by iterating over cells.
        For claimed boards: draw large symbol without filling the background so grid remains visible.
        active_board: (row, col) tuple for the board player must play in, or None for any available board."""
        small_board_size = 3 * self.mega_cell_size
        
        for mega_row in range(3):
            for mega_col in range(3):
                base_x = self.mega_board_offset_x + mega_col * small_board_size
                base_y = self.mega_board_offset_y + mega_row * small_board_size
                
                # If board is claimed, draw large symbol (without background fill so grid is visible)
                if claimed_boards[mega_row][mega_col] != " ":
                    if claimed_boards[mega_row][mega_col] == "D":
                        # Draw: white rectangle that doesn't touch outer borders
                        padding = self.mega_cell_size // 2
                        draw_rect = pygame.Rect(base_x + padding, base_y + padding,
                                               small_board_size - 2*padding, small_board_size - 2*padding)
                        pygame.draw.rect(self.screen, (255, 255, 255), draw_rect, 2)
                    else:
                        # Draw large symbol (O or X) without background fill
                        self.draw_mega_large_symbol(base_x, base_y, small_board_size, 
                                                   claimed_boards[mega_row][mega_col])
                else:
                    # Draw unclaimed board cells normally
                    for row in range(3):
                        for col in range(3):
                            self.draw_mega_board_cell(mega_row, mega_col, row, col, 
                                                    board[mega_row][mega_col][row][col])
        
        # Draw active board highlight
        if active_board is not None:
            self.draw_mega_board_highlight(active_board[0], active_board[1])
        
        # Redraw grid lines on top so they're always visible
        self.draw_mega_lines()

    def draw_mega_large_symbol(self, base_x, base_y, board_size, symbol):
        """Draw a large symbol (O or X) to fill a claimed board.
        No background fill so grid lines remain visible."""
        center_x = base_x + board_size // 2
        center_y = base_y + board_size // 2
        
        if symbol == "O":
            # Draw large circle
            radius = board_size // 3
            width = max(2, board_size // 15)
            pygame.draw.circle(self.screen, self.circle_color, (center_x, center_y), radius, width)
        elif symbol == "X":
            # Draw large X
            offset = board_size // 4  # Smaller offset to make X larger
            width = max(4, board_size // 10)  # Thicker lines
            # First diagonal
            pygame.draw.line(self.screen, self.cross_color, 
                           (base_x + offset, base_y + offset),
                           (base_x + board_size - offset, base_y + board_size - offset),
                           width)
            # Second diagonal
            pygame.draw.line(self.screen, self.cross_color,
                           (base_x + offset, base_y + board_size - offset),
                           (base_x + board_size - offset, base_y + offset),
                           width)

    def draw_mega_board_highlight(self, mega_row, mega_col):
        """Draw a highlight border around a specific mega board to show it's the active board."""
        small_board_size = 3 * self.mega_cell_size
        base_x = self.mega_board_offset_x + mega_col * small_board_size
        base_y = self.mega_board_offset_y + mega_row * small_board_size
        
        # Draw a glowing highlight border around the board
        highlight_width = 5
        # Outer glow (semi-transparent yellow)
        glow = pygame.Surface((small_board_size + 2*highlight_width, small_board_size + 2*highlight_width))
        glow.set_alpha(100)
        glow.fill((255, 255, 0))  # Yellow glow
        self.screen.blit(glow, (base_x - highlight_width, base_y - highlight_width))
        
        # Inner bright border
        pygame.draw.rect(self.screen, (255, 255, 100), 
                        (base_x - highlight_width, base_y - highlight_width, 
                         small_board_size + 2*highlight_width, small_board_size + 2*highlight_width), 
                        highlight_width)

    def draw_mega_circle(self, mega_row, mega_col, row, col):
        """Draw a circle in a specific cell of a specific small board."""
        small_board_size = 3 * self.mega_cell_size
        base_x = self.mega_board_offset_x + mega_col * small_board_size
        base_y = self.mega_board_offset_y + mega_row * small_board_size
        x = base_x + col * self.mega_cell_size + self.mega_cell_size // 2
        y = base_y + row * self.mega_cell_size + self.mega_cell_size // 2
        radius = max(4, self.mega_cell_size // 6)
        width = max(1, self.mega_cell_size // 20)
        pygame.draw.circle(self.screen, self.circle_color, (x, y), radius, width)

    def draw_mega_cross(self, mega_row, mega_col, row, col):
        """Draw a cross in a specific cell of a specific small board."""
        small_board_size = 3 * self.mega_cell_size
        base_x = self.mega_board_offset_x + mega_col * small_board_size
        base_y = self.mega_board_offset_y + mega_row * small_board_size
        
        space = max(3, self.mega_cell_size // 6)
        width = max(1, self.mega_cell_size // 20)
        
        x1 = base_x + col * self.mega_cell_size + space
        y1 = base_y + row * self.mega_cell_size + self.mega_cell_size - space
        x2 = base_x + col * self.mega_cell_size + self.mega_cell_size - space
        y2 = base_y + row * self.mega_cell_size + space
        pygame.draw.line(self.screen, self.cross_color, (x1, y1), (x2, y1), width)
        pygame.draw.line(self.screen, self.cross_color, (x1, y2), (x2, y2), width)

        x1 = base_x + col * self.mega_cell_size + space
        y1 = base_y + row * self.mega_cell_size + space
        x2 = base_x + col * self.mega_cell_size + self.mega_cell_size - space
        y2 = base_y + row * self.mega_cell_size + self.mega_cell_size - space
        pygame.draw.line(self.screen, self.cross_color, (x1, y1), (x2, y1), width)
        pygame.draw.line(self.screen, self.cross_color, (x1, y2), (x2, y2), width)

    def draw_mega_board_draw(self, mega_row, mega_col):
        """Draw a semi-transparent draw overlay on a drawn small board."""
        small_board_size = 3 * self.mega_cell_size
        base_x = self.mega_board_offset_x + mega_col * small_board_size
        base_y = self.mega_board_offset_y + mega_row * small_board_size
        
        overlay = pygame.Surface((small_board_size, small_board_size))
        overlay.set_alpha(40)
        overlay.fill((128, 128, 128))
        self.screen.blit(overlay, (base_x, base_y))

    def draw_player_status(self, current_player_name, active_symbol, symbol1, 
                          game_over, game_result, name1, name2, win_counts):
        """Draw the player status and score information."""
        if not game_over:
            status_text = f"{current_player_name}'s Turn ({active_symbol})  |  Press ESC to quit"
            color = self.circle_color if active_symbol == symbol1 else self.cross_color
        else:
            status_text = game_result
            color = self.text_color

        # Clip status text to window width
        clipped = self.clip_text(self.font_small, status_text, self.width - 40)
        text = self.font_small.render(clipped, True, color)
        text_rect = text.get_rect(center=(self.width // 2, 30))
        pygame.draw.rect(self.screen, self.bg_color, (0, 0, self.width, 60))
        self.screen.blit(text, text_rect)
        
        # Draw scores
        scores_text = f"{name1}: {win_counts.get(name1, 0)}  |  {name2}: {win_counts.get(name2, 0)}"
        scores_surface = self.font_tiny.render(scores_text, True, self.text_color)
        scores_rect = scores_surface.get_rect(center=(self.width // 2, 60))
        self.screen.blit(scores_surface, scores_rect)

    def draw_main_menu(self):
        """Draw the main menu and return button rectangles."""
        self.clear_screen()
        title = self.font_large.render('Tic-Tac-Toe v2.3', True, self.text_color)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title, title_rect)

        # Buttons (use more generous spacing)
        btn_w = min(600, int(self.width * 0.3))
        btn_h = max(70, int(self.height * 0.08))
        gap = int(btn_h * 0.6)
        top = int(self.height * 0.18)

        play_rect = pygame.Rect(self.width // 2 - btn_w // 2, top, btn_w, btn_h)
        scores_rect = pygame.Rect(self.width // 2 - btn_w // 2, top + (btn_h + gap), btn_w, btn_h)

        # Hover effect
        mpos = pygame.mouse.get_pos()
        needs_black_border = self.needs_black_button_border()
        play_color = self.button_hover_color if play_rect.collidepoint(mpos) else self.button_color
        scores_color = self.button_hover_color if scores_rect.collidepoint(mpos) else self.button_color

        pygame.draw.rect(self.screen, play_color, play_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), play_rect, 3)
        if needs_black_border:
            pygame.draw.rect(self.screen, (0, 0, 0), play_rect, 2)
        pygame.draw.rect(self.screen, scores_color, scores_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), scores_rect, 3)
        if needs_black_border:
            pygame.draw.rect(self.screen, (0, 0, 0), scores_rect, 2)

        play_text = self.font_small.render('Play', True, self.text_color)
        scores_text = self.font_small.render('Highscores', True, self.text_color)

        self.screen.blit(play_text, (play_rect.centerx - play_text.get_width() // 2,
                                     play_rect.centery - play_text.get_height() // 2))
        self.screen.blit(scores_text, (scores_rect.centerx - scores_text.get_width() // 2,
                                       scores_rect.centery - scores_text.get_height() // 2))

        # Settings button (no scores/game-results here)
        settings_rect = pygame.Rect(self.width // 2 - btn_w // 2, top + 2*(btn_h + gap), btn_w, btn_h)
        settings_color = self.button_hover_color if settings_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, settings_color, settings_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), settings_rect, 3)
        if needs_black_border:
            pygame.draw.rect(self.screen, (0, 0, 0), settings_rect, 2)
        settings_text = self.font_small.render('Settings', True, self.text_color)
        self.screen.blit(settings_text, (settings_rect.centerx - settings_text.get_width() // 2,
                                         settings_rect.centery - settings_text.get_height() // 2))

        # Quit button
        quit_rect = pygame.Rect(self.width // 2 - btn_w // 2, top + 3*(btn_h + gap), btn_w, btn_h)
        quit_color = self.button_hover_color if quit_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, quit_color, quit_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), quit_rect, 3)
        if needs_black_border:
            pygame.draw.rect(self.screen, (0, 0, 0), quit_rect, 2)
        quit_text = self.font_small.render('Quit', True, self.text_color)
        self.screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2,
                                     quit_rect.centery - quit_text.get_height() // 2))

        self.update_display()
        return play_rect, scores_rect, settings_rect, quit_rect

    def draw_highscores_screen(self, win_counts):
        """Draw the highscores screen and return the back button."""
        self.clear_screen()
        title = self.font_large.render('Highscores', True, self.text_color)
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)

        # List scores
        y = 140
        for player, count in win_counts.items():
            line = f"{player}: {count}"
            surf = self.font_small.render(line, True, self.text_color)
            rect = surf.get_rect(center=(self.width // 2, y))
            self.screen.blit(surf, rect)
            y += int(self.font_small.get_height() * 1.8)

        # Back button
        back_rect = pygame.Rect(self.width // 2 - 120, self.height - 140, 240, 70)
        mpos = pygame.mouse.get_pos()
        back_color = self.button_hover_color if back_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, back_color, back_rect)
        back_text = self.font_small.render('Back', True, self.text_color)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2,
                                     back_rect.centery - back_text.get_height() // 2))

        self.update_display()
        return back_rect

    def draw_highscores_menu(self):
        """Draw the highscores menu with options to view game results."""
        self.clear_screen()
        title = self.font_large.render('Highscores', True, self.text_color)
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)

        btn_w = min(600, int(self.width * 0.3))
        btn_h = max(70, int(self.height * 0.08))
        gap = int(btn_h * 0.4)
        top = int(self.height * 0.18)
        x = self.width // 2 - btn_w // 2

        regular_rect = pygame.Rect(x, top, btn_w, btn_h)
        mega_rect = pygame.Rect(x, top + btn_h + gap, btn_w, btn_h)

        mpos = pygame.mouse.get_pos()
        regular_color = self.button_hover_color if regular_rect.collidepoint(mpos) else self.button_color
        mega_color = self.button_hover_color if mega_rect.collidepoint(mpos) else self.button_color

        # Regular games button
        pygame.draw.rect(self.screen, regular_color, regular_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), regular_rect, 3)
        regular_text = self.font_small.render('Regular Games (last 10 days)', True, self.text_color)
        self.screen.blit(regular_text, (regular_rect.centerx - regular_text.get_width() // 2, regular_rect.centery - regular_text.get_height() // 2))

        # Mega games button
        pygame.draw.rect(self.screen, mega_color, mega_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), mega_rect, 3)
        mega_text = self.font_small.render('Mega Games (last 10 days)', True, self.text_color)
        self.screen.blit(mega_text, (mega_rect.centerx - mega_text.get_width() // 2, mega_rect.centery - mega_text.get_height() // 2))

        back_rect = pygame.Rect(self.width // 2 - 75, self.height - 120, 150, 50)
        back_color = self.button_hover_color if back_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, back_color, back_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 3)
        back_text = self.font_tiny.render('Back', True, self.text_color)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))

        self.update_display()
        return regular_rect, mega_rect, back_rect

    def draw_start_screen(self):
        """Draw the start screen with heading and advisory text."""
        # dark green background
        self.screen.fill((29,46,40))
        title = self.font_large.render('Tic-Tac-Toe v2.3 - 99% vibecoded', True, (255,255,255))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 40))
        self.screen.blit(title, title_rect)

        info = self.font_small.render('Press Space to continue', True, (255,255,255))
        info_rect = info.get_rect(center=(self.width // 2, self.height // 2 + 40))
        self.screen.blit(info, info_rect)

        self.update_display()
        return

    def draw_end_screen(self, board, symbol1, symbol2, game_result, current_player_name, 
                       active_symbol, name1, name2, win_counts):
        """Draw the end game screen with play again and quit options."""
        pygame.time.wait(500)
        self.clear_screen()
        self.draw_lines()
        self.draw_board(board, symbol1, symbol2)
        self.draw_player_status(current_player_name, active_symbol, symbol1,
                               True, game_result, name1, name2, win_counts)

        # Draw Play Again button (left) and Quit button (right)
        button_y = self.board_offset_y + 3 * CELL_SIZE + 40
        btn_w, btn_h = 120, 50
        spacing = 30
        
        # Play Again button on the left
        play_again_rect = pygame.Rect(
            self.width // 2 - btn_w - spacing // 2, 
            button_y, 
            btn_w, 
            btn_h
        )
        
        # Quit button on the right
        quit_rect = pygame.Rect(
            self.width // 2 + spacing // 2, 
            button_y, 
            btn_w, 
            btn_h
        )
        
        mpos = pygame.mouse.get_pos()
        play_color = self.button_hover_color if play_again_rect.collidepoint(mpos) else self.button_color
        quit_color = self.button_hover_color if quit_rect.collidepoint(mpos) else self.button_color

        # Draw Play Again button
        pygame.draw.rect(self.screen, play_color, play_again_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), play_again_rect, 3)
        play_again_text = self.font_tiny.render("Play Again (Y)", True, self.text_color)
        self.screen.blit(play_again_text, (play_again_rect.centerx - play_again_text.get_width() // 2,
                                           play_again_rect.centery - play_again_text.get_height() // 2))

        # Draw Quit button
        pygame.draw.rect(self.screen, quit_color, quit_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), quit_rect, 3)
        quit_text = self.font_tiny.render("Quit (Q)", True, self.text_color)
        self.screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2,
                                     quit_rect.centery - quit_text.get_height() // 2))

        self.update_display()
        return play_again_rect, quit_rect

    def draw_name_entry(self, p1_text, p2_text, active_player, error_message=None):
        """Draw the name entry screen and return input box rectangles."""
        self.clear_screen()
        title = self.font_large.render('Enter Player Names', True, self.text_color)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 60))

        info = self.font_small.render('Click a box and type names. Press Enter when done.', True, self.text_color)
        self.screen.blit(info, (self.width // 2 - info.get_width() // 2, 120))

        # Draw input boxes (use more space)
        box_w = min(900, int(self.width * 0.6))
        box_h = max(80, int(self.height * 0.1))
        rect1 = pygame.Rect(self.width // 2 - box_w // 2, 160, box_w, box_h)
        rect2 = pygame.Rect(self.width // 2 - box_w // 2, 160 + box_h + 40, box_w, box_h)

        mpos = pygame.mouse.get_pos()
        color1 = self.button_hover_color if rect1.collidepoint(mpos) else self.button_color
        color2 = self.button_hover_color if rect2.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, color1 if active_player == 1 else self.button_color, rect1)
        pygame.draw.rect(self.screen, (255, 255, 255), rect1, 3)
        pygame.draw.rect(self.screen, color2 if active_player == 2 else self.button_color, rect2)
        pygame.draw.rect(self.screen, (255, 255, 255), rect2, 3)

        t1_text = self.clip_text(self.font_small, p1_text or 'Player 1: ', rect1.width - 20)
        t2_text = self.clip_text(self.font_small, p2_text or 'Player 2: ', rect2.width - 20)
        t1 = self.font_small.render(t1_text, True, self.text_color)
        t2 = self.font_small.render(t2_text, True, self.text_color)
        self.screen.blit(t1, (rect1.x + 10, rect1.y + 12))
        self.screen.blit(t2, (rect2.x + 10, rect2.y + 12))

        prompt = self.font_tiny.render('Press Enter to continue', True, self.text_color)
        self.screen.blit(prompt, (self.width // 2 - prompt.get_width() // 2, rect2.y + box_h + 40))

        # Show validation error if present
        if error_message:
            err = self.font_tiny.render(error_message, True, (255, 100, 100))
            self.screen.blit(err, (self.width // 2 - err.get_width() // 2, rect2.y + box_h + 90))

        self.update_display()
        return rect1, rect2

    def draw_symbols_menu(self, s1, s2, active, error_message=None):
        """Draw the symbols selection screen and return input box rectangles."""
        self.clear_screen()
        title = self.font_large.render('Choose Player Symbols', True, self.text_color)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 60))

        # Improved centered instructions with room on both sides
        info = self.font_small.render('Click a box and type a single character. Press Enter when done.', True, self.text_color)
        self.screen.blit(info, (self.width // 2 - info.get_width() // 2, 120))

        # Draw symbol input boxes spaced further from center to allow room on both sides
        box_w = min(300, int(self.width * 0.18))
        box_h = max(100, int(self.height * 0.12))
        rect1 = pygame.Rect(self.width // 2 - box_w - 20, 160, box_w, box_h)
        rect2 = pygame.Rect(self.width // 2 + 20, 160, box_w, box_h)

        mpos = pygame.mouse.get_pos()
        color1 = self.button_hover_color if rect1.collidepoint(mpos) else self.button_color
        color2 = self.button_hover_color if rect2.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, color1 if active == 1 else self.button_color, rect1)
        pygame.draw.rect(self.screen, (255, 255, 255), rect1, 3)
        pygame.draw.rect(self.screen, color2 if active == 2 else self.button_color, rect2)
        pygame.draw.rect(self.screen, (255, 255, 255), rect2, 3)

        t1 = self.font_large.render(s1 or 'O', True, self.text_color)
        t2 = self.font_large.render(s2 or 'X', True, self.text_color)
        # Center symbol text inside each box vertically and horizontally
        self.screen.blit(t1, (rect1.x + rect1.width // 2 - t1.get_width() // 2, rect1.y + rect1.height // 2 - t1.get_height() // 2))
        self.screen.blit(t2, (rect2.x + rect2.width // 2 - t2.get_width() // 2, rect2.y + rect2.height // 2 - t2.get_height() // 2))

        if error_message:
            err = self.font_tiny.render(error_message, True, (255, 100, 100))
            self.screen.blit(err, (self.width // 2 - err.get_width() // 2, rect2.y + rect2.height + 20))

        prompt = self.font_tiny.render('Press Enter to continue', True, self.text_color)
        self.screen.blit(prompt, (self.width // 2 - prompt.get_width() // 2, rect2.y + rect2.height + 60))

        self.update_display()
        return rect1, rect2

    def draw_file_view(self, title, lines, offset):
        """Draw a generic file view with wrapped text and paging.

        Returns: (back_rect, total_lines, max_visible_lines)
        """
        self.clear_screen()
        title_surf = self.font_large.render(title, True, self.text_color)
        self.screen.blit(title_surf, ((self.width - title_surf.get_width()) // 2, 60))

        y = 140
        line_height = int(self.font_small.get_height() * 1.6)
        avail_height = self.height - 220
        max_lines = max(1, avail_height // line_height)

        # Wrap lines to fit within the window with margins
        wrapped = []
        margin = 80
        max_width = self.width - margin*2
        for line in lines:
            # preserve empty lines
            if not line:
                wrapped.append('')
                continue
            words = line.split(' ')
            cur = ''
            for w in words:
                test = (cur + ' ' + w).strip() if cur else w
                if self.font_small.size(test)[0] <= max_width:
                    cur = test
                else:
                    if cur:
                        wrapped.append(cur)
                    cur = w
            if cur:
                wrapped.append(cur)

        total = len(wrapped)
        visible = wrapped[offset:offset + max_lines]
        for ln in visible:
            surf = self.font_small.render(ln, True, self.text_color)
            self.screen.blit(surf, (40, y))
            y += line_height
        # Page info
        page_info = self.font_tiny.render(f"Lines {min(offset+1,total)}-{min(offset+max_lines,total)} of {total}", True, self.text_color)
        self.screen.blit(page_info, (self.width // 2 - page_info.get_width() // 2, self.height - 150))

        back_rect = pygame.Rect(self.width // 2 - 75, self.height - 120, 150, 50)
        mpos = pygame.mouse.get_pos()
        back_color = self.button_hover_color if back_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, back_color, back_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 3)
        back_text = self.font_tiny.render('Back', True, self.text_color)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2,
                                     back_rect.centery - back_text.get_height() // 2))

        self.update_display()
        return back_rect, total, max_lines

    # Colors menu removed — color customization is no longer provided in the UI.
    # If needed later, add a dedicated theme system with persisted settings.


    def draw_bot_difficulty_menu(self, current='medium'):
        """Draw menu to choose bot difficulty and return option rects and back rect."""
        self.clear_screen()
        title = self.font_large.render('Bot Difficulty', True, self.text_color)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 60))

        # Options: Easy, Medium, Hard
        btn_w = min(500, int(self.width * 0.4))
        btn_h = max(70, int(self.height * 0.09))
        gap = int(btn_h * 0.5)
        x = self.width // 2 - btn_w // 2
        y = 160

        easy_rect = pygame.Rect(x, y, btn_w, btn_h)
        med_rect = pygame.Rect(x, y + btn_h + gap, btn_w, btn_h)
        hard_rect = pygame.Rect(x, y + 2 * (btn_h + gap), btn_w, btn_h)

        mpos = pygame.mouse.get_pos()
        for r, label in ((easy_rect, 'Easy'), (med_rect, 'Medium'), (hard_rect, 'Hard')):
            color = self.button_hover_color if r.collidepoint(mpos) else self.button_color
            pygame.draw.rect(self.screen, color, r)
            pygame.draw.rect(self.screen, (255, 255, 255), r, 3)
            text = self.font_small.render(label, True, self.text_color)
            self.screen.blit(text, (r.centerx - text.get_width() // 2, r.centery - text.get_height() // 2))

        # highlight current
        if current:
            cur_text = self.font_tiny.render(f'Current: {current.title()}', True, self.text_color)
            self.screen.blit(cur_text, (self.width // 2 - cur_text.get_width() // 2, hard_rect.y + hard_rect.height + 20))

        back_rect = pygame.Rect(self.width // 2 - 75, self.height - 120, 150, 50)
        back_color = self.button_hover_color if back_rect.collidepoint(mpos) else self.button_color
        pygame.draw.rect(self.screen, back_color, back_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 3)
        back_text = self.font_tiny.render('Back', True, self.text_color)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))

    def clip_text(self, font, text, max_width):
        """Return text truncated with ellipsis if it exceeds max_width when rendered with font."""
        if font.size(text)[0] <= max_width:
            return text
        ell = '...'
        max_w = max_width - font.size(ell)[0]
        s = text
        while s and font.size(s)[0] > max_w:
            s = s[:-1]
        return s + ell

    # remaining methods copied verbatim...



