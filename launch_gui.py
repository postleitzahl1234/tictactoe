

#python launch_gui.py


from GUI.gui import TicTacToeGUI, MegaTicTacToeGUI
import pygame


def main():
    pygame.init()
    
    # Start with regular tic tac toe by default
    game_type = 'regular'
    
    while True:
        # Create the appropriate game based on selection
        if game_type == 'regular':
            game = TicTacToeGUI("Player 1", "Player 2", "O", "X")
        else:
            game = MegaTicTacToeGUI("Player 1", "Player 2", "O", "X")
        
        # Store the current game type so settings can change it
        game.game_type = game_type
        
        try:
            game.show_start_screen()
        except Exception:
            pass
        
        game.game_loop_gui()
        
        # Check if game_type was changed in settings and restart
        if hasattr(game, 'game_type_changed') and game.game_type_changed:
            game_type = game.new_game_type
            game.game_type_changed = False
        else:
            break
    
    pygame.quit()


if __name__ == "__main__":
    main()
