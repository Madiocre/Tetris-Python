import time
import cv2

class SimpleTetrisPlayer:
    def __init__(self, game, render=False, delay=0.1):
        self.game = game
        self.render = render
        self.delay = delay

    def evaluate_board(self, board_props):
        """Heuristic evaluation function using board properties"""
        # Unpack the properties
        lines, holes, total_bumpiness, sum_height = board_props

        # Define weights for different criteria
        weight_lines = 1.0
        weight_holes = -1.0
        weight_bumpiness = -0.5
        weight_height = -0.5

        # Calculate score based on properties
        score = (weight_lines * lines +
                 weight_holes * holes +
                 weight_bumpiness * total_bumpiness +
                 weight_height * sum_height)
        return score

    def choose_best_move(self, next_states):
        """Choose the best move based on heuristic evaluation"""
        best_score = float('-inf')
        best_move = None
        
        for move, board_props in next_states.items():
            score = self.evaluate_board(board_props)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

    def play_game(self):
        """Play the game using the heuristic algorithm"""
        self.game.reset()

        while not self.game.game_over:
            next_states = self.game.get_next_states()
            if not next_states:
                break
            
            best_move = self.choose_best_move(next_states)
            if best_move:
                x, rotation = best_move
                _, done = self.game.play(x, rotation, render=False)

            if self.render:
                self.game.render()  # Call the render method from Tetris class

            time.sleep(self.delay)
            
            key = cv2.waitKey(1)  # Adjust delay as needed
            if key == 27:  # ESC key to exit
                exit(1)

        return self.game.get_game_score()
