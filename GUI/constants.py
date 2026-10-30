# Screen dimensions
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

# Grid configuration
GRID_SIZE = 3
CELL_SIZE = 150
# center the board dynamically based on window size
BOARD_WIDTH = GRID_SIZE * CELL_SIZE
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE
BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2
BOARD_OFFSET_Y = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2
LINE_WIDTH = 15
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = CELL_SIZE // 4

# Colors - Themes
THEMES = {
    'forest': {
        'bg': (29, 46, 40),          # Dark green
        'line': (255, 255, 255),     # White
        'circle': (255, 255, 255),   # White
        'cross': (255, 255, 255),    # White
        'text': (255, 255, 255),     # White
        'button': (64, 145, 108),    # Green
        'button_hover': (76, 174, 129),  # Lighter green
    },
    'soft desert': {
        'bg': (245, 240, 225),       # #F5F0E1 warm off-white
        'line': (165, 165, 141),     # #A5A58D soft olive-gray
        'circle': (107, 144, 128),   # #6B9080 desaturated teal
        'cross': (208, 140, 101),    # #D08C65 muted terracotta
        'text': (60, 50, 40),        # Dark text for light background
        'button': (165, 165, 141),   # #A5A58D soft olive-gray
        'button_hover': (208, 140, 101),  # #D08C65 muted terracotta
    },
    'misty pastel': {
        'bg': (46, 47, 54),          # #2E2F36 deep charcoal
        'line': (92, 92, 114),       # #5C5C72 muted slate
        'circle': (247, 197, 159),   # #F7C59F pale peach
        'cross': (199, 206, 234),    # #C7CEEA light lavender
        'text': (255, 255, 255),     # White
        'button': (92, 92, 114),     # #5C5C72 muted slate
        'button_hover': (199, 206, 234),  # #C7CEEA light lavender
    },
    'ocean breeze': {
        'bg': (227, 246, 245),       # #E3F6F5 pale aqua
        'line': (159, 184, 173),     # #9FB8AD soft seafoam
        'circle': (74, 111, 165),    # #4A6FA5 dusty blue
        'cross': (242, 141, 53),     # #F28D35 sunset orange
        'text': (30, 50, 60),        # Dark text for light background
        'button': (159, 184, 173),   # #9FB8AD soft seafoam
        'button_hover': (242, 141, 53),  # #F28D35 sunset orange
    },
}

# Default theme
DEFAULT_THEME = 'forest'
# Font sizes
FONT_LARGE = 56
FONT_SMALL = 36
FONT_TINY = 24


