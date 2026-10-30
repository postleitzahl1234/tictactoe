"""Sound Effects and Music Module for TicTacToe Game."""

import pygame
import os


class SFXManager:
    """Manages sound effects and music for the game."""
    
    def __init__(self):
        """Initialize the SFX manager with sound enabled by default."""
        self.sound_enabled = True
        self.music_playing = False
        self.current_music = None
        
        # Get the directory where this file is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.music_dir = os.path.join(os.path.dirname(base_dir), 'music')
    
    def toggle_sound(self):
        """Toggle sound on/off and stop music if disabling."""
        self.sound_enabled = not self.sound_enabled
        if not self.sound_enabled:
            self.stop_music()
        return self.sound_enabled
    
    def is_sound_enabled(self):
        """Return whether sound is currently enabled."""
        return self.sound_enabled
    
    def play_music(self, filename='music.wav', loops=-1):
        """
        Play background music.
        
        Args:
            filename: Name of the music file in the music directory
            loops: Number of times to loop (-1 for infinite)
        """
        if not self.sound_enabled:
            return
        
        music_path = os.path.join(self.music_dir, filename)
        
        if not os.path.exists(music_path):
            # Sound files are optional (see music/README.md); play nothing.
            return
        
        try:
            # Stop any currently playing music
            if self.music_playing:
                pygame.mixer.music.stop()
            
            # Load and play the new music
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loops)
            self.music_playing = True
            self.current_music = filename
        except Exception as e:
            print(f"Error playing music: {e}")
    
    def stop_music(self):
        """Stop the currently playing music."""
        try:
            if self.music_playing:
                pygame.mixer.music.stop()
                self.music_playing = False
                self.current_music = None
        except Exception as e:
            print(f"Error stopping music: {e}")
    
    def pause_music(self):
        """Pause the currently playing music."""
        try:
            if self.music_playing:
                pygame.mixer.music.pause()
        except Exception as e:
            print(f"Error pausing music: {e}")
    
    def unpause_music(self):
        """Resume the currently paused music."""
        try:
            if self.music_playing:
                pygame.mixer.music.unpause()
        except Exception as e:
            print(f"Error unpausing music: {e}")
    
    def set_music_volume(self, volume):
        """
        Set the music volume.
        
        Args:
            volume: Float between 0.0 (silent) and 1.0 (full volume)
        """
        try:
            volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
            pygame.mixer.music.set_volume(volume)
        except Exception as e:
            print(f"Error setting music volume: {e}")
    
    def play_background_music(self):
        """Play the background music (looping), if music/background.mp3 exists."""
        self.play_music('background.mp3', loops=-1)
    
    def play_win_sound(self):
        """Play the victory sound once, if music/win.mp3 exists."""
        self.play_music('win.mp3', loops=0)
    
    def play_lose_sound(self):
        """Play the game-over sound once, if music/lose.mp3 exists."""
        self.play_music('lose.mp3', loops=0)


# Global instance
_sfx_manager = None


def get_sfx_manager():
    """Get or create the global SFX manager instance."""
    global _sfx_manager
    if _sfx_manager is None:
        _sfx_manager = SFXManager()
    return _sfx_manager
