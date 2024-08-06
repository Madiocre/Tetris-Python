from tetris import Tetris
from ai_control import SimpleTetrisPlayer  # Assuming the class is in this file
import threading

def main():
    tetris_game = Tetris()
    
    # Initialize players
    ai_player = SimpleTetrisPlayer(tetris_game, render=True, delay=0.5)    
    # You can run both players in sequence or as needed
    # Here is an example of running them in sequence
    ai_player.play_game()  # AI player plays the game

if __name__ == "__main__":
    main()