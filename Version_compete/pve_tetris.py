import pygame
import random

# Define colors
colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
    
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2 * 100

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def get_board_props(self):
            '''Get properties of the board for AI evaluation'''
            return [0, 0, 0, 0]  # Placeholder, update based on your properties

    def get_next_states(self):
        '''Get all possible next states'''
        states = {}
        piece_id = self.figure.type
        rotations = [0, 90, 180, 270]

        for rotation in rotations:
            piece = self.figure.figures[piece_id][rotation]
            min_x = min([p % 4 for p in piece])
            max_x = max([p % 4 for p in piece])

            for x in range(-min_x, self.width - max_x):
                pos = [x, 0]

                while not self.intersects():
                    pos[1] += 1
                pos[1] -= 1

                if pos[1] >= 0:
                    board = [row[:] for row in self.field]
                    for i, j in piece:
                        board[i + pos[1]][j + pos[0]] = self.figure.color
                    states[(x, rotation)] = self.get_board_props()

        return states

class TetrisBot:
    pass

# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define the size of the window and the split dimensions
WINDOW_WIDTH = 800  # Increased width to fit two games
WINDOW_HEIGHT = 500
VIEW_WIDTH = WINDOW_WIDTH // 2
VIEW_HEIGHT = WINDOW_HEIGHT

# Create the main window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PVP Tetris")

# Create surfaces for each game view
game_view1 = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))
game_view2 = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))

# Instantiate two games
game1 = Tetris(20, 10)
game2 = Tetris(20, 10)

# Initialize game variables
clock = pygame.time.Clock()
fps = 25
counter = 0

pressing_down1 = False
pressing_down2 = False

while True:
    if game1.figure is None:
        game1.new_figure()
    if game2.figure is None:
        game2.new_figure()

    counter += 1
    if counter > 100000:
        counter = 0

    # Update both games
    if counter % (fps // game1.level // 2) == 0 or pressing_down1:
        if game1.state == "start":
            game1.go_down()
    if counter % (fps // game2.level // 2) == 0 or pressing_down2:
        if game2.state == "start":
            game2.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            # Controls for the first game (using arrow keys)
            if event.key == pygame.K_UP:
                game1.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down1 = True
            if event.key == pygame.K_LEFT:
                game1.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game1.go_side(1)
            if event.key == pygame.K_SPACE:
                game1.go_space()

            # Controls for the second game (using WASD keys)
            if event.key == pygame.K_w:
                game2.rotate()
            if event.key == pygame.K_s:
                pressing_down2 = True
            if event.key == pygame.K_a:
                game2.go_side(-1)
            if event.key == pygame.K_d:
                game2.go_side(1)
            if event.key == pygame.K_q:  # Use 'Q' for space (or any other key if you prefer)
                game2.go_space()

            if event.key == pygame.K_ESCAPE:
                game1.__init__(20, 10)
                game2.__init__(20, 10)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down1 = False
            if event.key == pygame.K_s:
                pressing_down2 = False

    # Fill each game view surface with white
    game_view1.fill(WHITE)
    game_view2.fill(WHITE)

    # Draw the first game
    for i in range(game1.height):
        for j in range(game1.width):
            pygame.draw.rect(game_view1, GRAY, [game1.x + game1.zoom * j, game1.y + game1.zoom * i, game1.zoom, game1.zoom], 1)
            if game1.field[i][j] > 0:
                pygame.draw.rect(game_view1, colors[game1.field[i][j]],
                                 [game1.x + game1.zoom * j + 1, game1.y + game1.zoom * i + 1, game1.zoom - 2, game1.zoom - 1])

    if game1.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game1.figure.image():
                    pygame.draw.rect(game_view1, colors[game1.figure.color],
                                     [game1.x + game1.zoom * (j + game1.figure.x) + 1,
                                      game1.y + game1.zoom * (i + game1.figure.y) + 1,
                                      game1.zoom - 2, game1.zoom - 2])

    # Draw the second game
    for i in range(game2.height):
        for j in range(game2.width):
            pygame.draw.rect(game_view2, GRAY, [game2.x + game2.zoom * j, game2.y + game2.zoom * i, game2.zoom, game2.zoom], 1)
            if game2.field[i][j] > 0:
                pygame.draw.rect(game_view2, colors[game2.field[i][j]],
                                 [game2.x + game2.zoom * j + 1, game2.y + game2.zoom * i + 1, game2.zoom - 2, game2.zoom - 1])

    if game2.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game2.figure.image():
                    pygame.draw.rect(game_view2, colors[game2.figure.color],
                                     [game2.x + game2.zoom * (j + game2.figure.x) + 1,
                                      game2.y + game2.zoom * (i + game2.figure.y) + 1,
                                      game2.zoom - 2, game2.zoom - 2])

    # Draw scores and game states
    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text1 = font.render("Score: " + str(game1.score), True, BLACK)
    text2 = font.render("Score: " + str(game2.score), True, BLACK)
    text_game_over1 = font1.render("Game Over", True, (255, 125, 0))
    text_game_over2 = font1.render("Press ESC", True, (255, 215, 0))

    game_view1.blit(text1, [0, 0])
    if game1.state == "gameover":
        game_view1.blit(text_game_over1, [20, 200])
        game_view1.blit(text_game_over2, [25, 265])

    game_view2.blit(text2, [0, 0])
    if game2.state == "gameover":
        game_view2.blit(text_game_over1, [20, 200])
        game_view2.blit(text_game_over2, [25, 265])

    # Blit the surfaces to the main screen
    screen.blit(game_view1, (0, 0))
    screen.blit(game_view2, (VIEW_WIDTH, 0))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
