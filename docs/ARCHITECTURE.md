# Architecture overview

## Project Summary
A feature-rich TicTacToe game application with both regular 3x3 and Mega 9x9 game variants implemented in Python using Pygame. The application includes a GUI with themes, multiplayer/singleplayer modes, AI bot with difficulty levels, sound effects, and comprehensive game result tracking.

---

## Main Entry Points & Applications

### 1. **launch_gui.py** (Primary Entry Point)
- **Purpose**: Launches the Pygame GUI application with game type selection
- **Key Functionality**:
  - Initializes Pygame
  - Manages game type switching ('regular' vs 'mega' TicTacToe)
  - Implements game loop that allows restarting with different game modes
  - Handles graceful shutdown with proper pygame cleanup

**To Run**: `python launch_gui.py`

---

## Key Modules & Architecture

### Core Game Logic

#### **GUI/main.py** (Game Logic Foundation)
Contains the base game logic classes used by both regular and mega variants:

1. **`TicTacToe` Class**
   - Base class for all game logic
   - Properties: board (3x3), symbols, player management, win tracking
   - Key Methods:
     - `set_starting_position()` - Initialize board and starting player
     - `play_single_game()` - Terminal-based single game loop
     - `game_loop()` - Terminal-based multi-game loop (legacy)
     - `is_winning()` - Check for winning condition
     - `change_active_player()` - Toggle between players
     - `get_available_moves()` - List all empty cells
     - `get_bot_move(difficulty)` - AI logic for regular game ('easy', 'medium', 'hard')
     - `register_win(symbol)` - Update win counters
     - `write_game_result(winner_symbol)` - Log game to file
     - `current_player_name()` - Get active player name

2. **`MegaTicTacToe` Class**
   - Extends TicTacToe for 9x9 super-grid variant
   - Properties: 
     - `boards` (9 sub-boards, each 3x3)
     - `board` (3x3 meta-board tracking claimed sub-boards)
     - `claimed_boards` (tracks which player controls each meta-board)
     - `active_board` (restricts player moves to specific sub-board)
   - Key Methods:
     - `is_winning_mega()` - Check win on meta-board
     - `is_position_valid(row, col)` - Validate move legality
     - `get_next_board(row, col)` - Determine which sub-board player moves to
     - `get_bot_move_mega(difficulty)` - AI for mega variant

---

### GUI & Rendering

#### **GUI/gui.py** (Main GUI Classes)
Pygame-based GUI implementation inheriting from game logic classes:

1. **`TicTacToeGUI` Class**
   - GUI wrapper for regular 3x3 TicTacToe
   - Initializes:
     - `ScreenRenderer` for drawing
     - `InputHandler` for event processing
     - `SFXManager` for sound effects
   - Key GUI Methods:
     - `show_start_screen()` - Title/menu screen with options
     - `play_single_game_gui()` - Main game loop with event handling
     - `game_loop_gui()` - Multi-game loop with menus
     - `show_settings_menu()` - Theme, difficulty, sound, multiplayer toggle
     - `show_highscores_screen()` - View past game results
     - `show_last_games_screen()` - Recent game boards (last 10 days)

2. **`MegaTicTacToeGUI` Class**
   - GUI wrapper for 9x9 Mega variant
   - Similar structure to TicTacToeGUI
   - Renders 9x9 grid with enhanced coordinate tracking

---

#### **GUI/renderers/screen.py** (ScreenRenderer Class)
Handles all Pygame rendering operations:
- **Properties**:
  - Fullscreen display (adaptive to resolution)
  - Dynamic scaling for 9x9 mega board
  - Centered board positioning
  - Theme color management

- **Key Methods**:
  - `clear_screen()` - Reset display
  - `draw_lines()` - Draw 3x3 grid lines
  - `draw_mega_lines()` - Draw 9x9 grid with sub-grid borders
  - `draw_board(board, s1, s2)` - Render board state with symbols
  - `draw_player_status()` - Display current player, scores, game result
  - `draw_start_screen()` - Title and main menu
  - `draw_settings_menu()` - Settings options with buttons
  - `draw_highscores_menu()` - High scores menu
  - `set_theme(theme_name)` - Switch between 4 color themes
  - `update_display()` - Refresh pygame display

- **Themes Available** (in `constants.py`):
  1. Forest (dark green background)
  2. Soft Desert (warm off-white, muted terracotta)
  3. Misty Pastel (deep charcoal, peach & lavender)
  4. Ocean Breeze (pale aqua, dusty blue & sunset orange)

---

#### **GUI/handlers/input_handler.py**
Handles user input and event processing:
- **Key Methods**:
  - `get_cell_from_click(pos)` - Convert mouse position to board coordinates
  - `mark_cell(board, row, col, symbol, move_count)` - Place symbol and validate
  - `handle_menu_input(event, play_rect, scores_rect, ...)` - Menu navigation
  - `handle_settings_input(event, ...)` - Settings menu handling
  - `handle_end_screen_input(event, ...)` - End game screen input

---

#### **GUI/constants.py** (Configuration)
Defines game constants:
- Screen dimensions (700x700, fullscreen capable)
- Grid configuration (3x3 cells, 150px per cell)
- Rendering parameters (line widths, circle/cross dimensions)
- Font sizes (LARGE: 56px, SMALL: 36px, TINY: 24px)
- 4 Color themes with RGB values

---

### Sound & Music

#### **GUI/sfx.py** (SFXManager Class)
Manages background music and sound effects:
- **Properties**:
  - `sound_enabled` - Toggle sound on/off
  - `music_playing` - Current playback state
  - `music_dir` - Path to music folder

- **Key Methods**:
  - `toggle_sound()` - Enable/disable all sound
  - `is_sound_enabled()` - Query current status
  - `play_music(filename, loops)` - Play background music
  - `play_win_sound()` - Victory sound (singleplayer only)
  - `play_lose_sound()` - Defeat sound (singleplayer only)
  - `stop_music()` - Stop current playback
  - `pause_music()` / `unpause_music()` - Pause control
  - `set_music_volume(volume)` - Volume control (0.0-1.0)
  - `get_sfx_manager()` - Global singleton accessor

- **Sound files** (optional): `music/background.mp3`, `music/win.mp3`, `music/lose.mp3`; missing files are skipped silently

---

## File Structure

```
tictactoe_v2.3/
├── launch_gui.py              # Main entry point
├── GUI/
│   ├── main.py               # Core game logic (TicTacToe, MegaTicTacToe)
│   ├── gui.py                # GUI implementations (TicTacToeGUI, MegaTicTacToeGUI)
│   ├── constants.py          # Game configuration & themes
│   ├── sfx.py                # Sound effects manager
│   ├── handlers/
│   │   ├── input_handler.py  # Input handling logic
│   │   └── __init__.py
│   ├── renderers/
│   │   ├── screen.py         # Pygame rendering
│   │   └── __init__.py
│   └── __init__.py
├── music/                    # Optional sound files (see music/README.md)
├── docs/ARCHITECTURE.md      # This file
├── (game_results.txt, mega_game_results.txt, daily_scores.json are created at runtime)
└── __pycache__/              # Python cache

```

---

## Game Modes & Features

### Game Variants
1. **Regular TicTacToe** - Classic 3x3 grid, 2 players
2. **Mega TicTacToe** - 9x9 grid of 3x3 boards, constraints on next board

### Player Modes
- **Multiplayer** - Two human players alternate turns
- **Singleplayer** - One human player vs AI bot

### AI Difficulty Levels
- **Easy** - Random valid moves
- **Medium** - Mix of smart and random moves (blocks winning moves, takes winning opportunity)
- **Hard** - Strategic play (evaluates board state, tends toward center)

### Customization
- **4 Color Themes** - Forest, Soft Desert, Misty Pastel, Ocean Breeze
- **Sound Toggle** - Enable/disable background music and effects
- **Settings Menu** - Change theme, difficulty, game mode, sound

---

## Dependencies

### Required Python Packages
- **pygame** - Pygame library for graphics and event handling
- Standard library only: `datetime`, `json`, `os`, `random`, `sys`

Install with `pip install -r requirements.txt`.

### Tests
- `python test_suite.py` runs 34 `unittest` tests (game logic, bot, mega rules, input mapping, themes, file I/O)

---

## Data Storage

### Daily Scores (daily_scores.json)
```json
{
  "2026-01-09": {
    "Player 1": 2,
    "Player 2": 1
  },
  "2026-01-10": {
    "Player 1": 1,
    "Player 2": 1
  }
}
```

### Game Results (game_results.txt & mega_game_results.txt)
- Timestamp-based entries
- Winner information (symbol & player name)
- Full board state at end of game
- Entries separated by `---` delimiter
- Used for 10-day game history view

---

## Current State & Notes

✅ **Implemented**:
- Full GUI with Pygame
- Regular and Mega TicTacToe variants
- Multiplayer and singleplayer modes
- AI bot with 3 difficulty levels
- 4 color themes with dynamic switching
- Game result tracking and history
- Sound/music management system
- Settings menu with multiple options
- Fullscreen support with responsive layout

⚠️ **Missing**:
- Unit tests / Test suite
- Dependencies file (requirements.txt)
- Music files are not shipped (see music/README.md)
- Auto-save/persistence for player names
- Online multiplayer
- Game statistics/replay features

---

## How to Use (Getting Started)

1. **Install Dependencies**:
   ```bash
   pip install pygame
   ```

2. **Add Music Files** (optional):
   - Place `background.mp3`, `win.mp3` and `lose.mp3` in the `music/` folder for sound

3. **Run the Game**:
   ```bash
   python launch_gui.py
   ```

4. **Game Flow**:
   - Start screen → Select game type (Regular/Mega)
   - Choose multiplayer or singleplayer (with AI difficulty)
   - Play game with mouse clicks on board cells
   - Press ESC to quit to menu
   - Access settings for theme, sound, and mode changes
   - View past games in "High Scores" section

---

## Architecture Decisions

- **Inheritance-based**: GUI classes inherit from game logic classes, allowing code reuse
- **Singleton SFXManager**: Single global sound manager prevents multiple music instances
- **Fullscreen Responsive**: Board automatically centers and scales based on display resolution
- **Theme System**: Centralized color definitions enable easy visual customization
