import pygame
import random

#TODO add autorotation functionality similar to how mouse input works at https://tetris.com/play-tetris
#TODO add a way for the user to hold 1 piece at a time and recall it as they wish
#TODO add a way for the user to see what the next 3 pieces will be
#TODO when space key is pressed drop down current piece

# Initialize pygame
pygame.init()

# Screen dimensions and block size
SCREEN_WIDTH = 300  # Width of the game window
SCREEN_HEIGHT = 600  # Height of the game window
BLOCK_SIZE = 30  # Size of each block in the grid

# Colors used in the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Define the Tetrimino shapes using 2D lists
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]],  # J shape
]

# Assign colors to each shape
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, ORANGE, BLUE]

# Initialize the grid with black (empty space)
grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]


# Function to draw the grid and the placed Tetriminos
def draw_grid(surface):
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            pygame.draw.rect(surface, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(surface, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)  # Grid lines


# Function to check if a given position causes a collision
def check_collision(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:  # If part of the shape exists
                new_x, new_y = x + off_x, y + off_y
                if new_x < 0 or new_x >= len(grid[0]) or new_y >= len(grid) or grid[new_y][new_x] != BLACK:
                    return True  # Collision detected
    return False


# Function to clear completed lines from the grid
def clear_lines():
    global grid
    grid = [row for row in grid if any(color == BLACK for color in row)]  # Keep only non-full rows
    while len(grid) < SCREEN_HEIGHT // BLOCK_SIZE:  # Add empty rows at the top
        grid.insert(0, [BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])


# Function to rotate a shape 90 degrees clockwise
def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]


# Class to represent a falling Tetrimino
class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)  # Randomly select a shape
        self.color = SHAPE_COLORS[SHAPES.index(self.shape)]  # Assign corresponding color
        self.x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(self.shape[0]) // 2  # Start in the middle
        self.y = 0  # Start from the top

    # Draw the Tetrimino on the screen
    def draw(self, surface):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.color,
                                     ((self.x + x) * BLOCK_SIZE, (self.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Move the Tetrimino left, right, or down if possible
    def move(self, dx, dy):
        if not check_collision(self.shape, (self.x + dx, self.y + dy)):
            self.x += dx
            self.y += dy

    # Rotate the Tetrimino if there is no collision
    def rotate(self):
        rotated_shape = rotate_shape(self.shape)
        if not check_collision(rotated_shape, (self.x, self.y)):
            self.shape = rotated_shape


# Main game loop setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

current_tetrimino = Tetrimino()  # Start with a random Tetrimino
fall_time = 0  # Timer for automatic falling

running = True
while running:
    screen.fill(BLACK)  # Clear the screen
    draw_grid(screen)  # Draw the grid
    current_tetrimino.draw(screen)  # Draw the active Tetrimino
    pygame.display.flip()  # Update the screen

    fall_time += clock.get_rawtime()
    clock.tick(30)  # Set game speed

    # Event handling for quitting and key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetrimino.move(-1, 0)  # Move left
            if event.key == pygame.K_RIGHT:
                current_tetrimino.move(1, 0)  # Move right
            if event.key == pygame.K_DOWN:
                current_tetrimino.move(0, 1)  # Move down faster
            if event.key == pygame.K_UP:
                current_tetrimino.rotate()  # Rotate

    # Handle automatic falling
    if fall_time > 500:  # Time threshold to drop the piece
        if not check_collision(current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y + 1)):
            current_tetrimino.y += 1  # Move down
        else:
            # Lock the piece in place
            for y, row in enumerate(current_tetrimino.shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[current_tetrimino.y + y][current_tetrimino.x + x] = current_tetrimino.color
            clear_lines()  # Clear completed rows
            current_tetrimino = Tetrimino()  # Spawn a new piece
            if check_collision(current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y)):
                running = False  # End game if new piece collides immediately
        fall_time = 0

pygame.quit()  # Exit the game