import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions and block size
SCREEN_WIDTH = 540  # Increased width to accommodate queue and hold areas
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)  # Border color

# Tetrimino shapes and colors
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]],  # J shape
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, ORANGE, BLUE]
GRID_WIDTH = 10  # Standard Tetris width
GRID_X_OFFSET = 120  # Offset to shift grid right, leaving space for hold display

# Initialize grid
grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]

score = 0
fall_speed = 500  # milliseconds


# Function to draw the grid and placed blocks
def draw_grid(surface):
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            pygame.draw.rect(surface, color,
                             (GRID_X_OFFSET + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(surface, WHITE,
                             (GRID_X_OFFSET + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Check for collisions
def check_collision(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x, new_y = x + off_x, y + off_y
                # Ensure new_x and new_y are within valid bounds
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= len(grid):
                    return True
                if new_y >= 0 and grid[new_y][new_x] != BLACK:  # Avoid accessing negative indices
                    return True
    return False



# Clear full lines
def clear_lines():
    global grid, score
    lines_cleared = 0
    new_grid = []
    for row in grid:
        if all(cell != BLACK for cell in row):
            lines_cleared += 1
        else:
            new_grid.append(row)
    while len(new_grid) < SCREEN_HEIGHT // BLOCK_SIZE:
        new_grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
    grid = new_grid

    # Update score based on standard Tetris rules
    if lines_cleared == 1:
        score += 100
    elif lines_cleared == 2:
        score += 300
    elif lines_cleared == 3:
        score += 500
    elif lines_cleared == 4:
        score += 800

    return lines_cleared


# Rotate shape
def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

class Tetrimino:
    def __init__(self, shape=None):
        self.shape = shape if shape else random.choice(SHAPES)
        self.color = SHAPE_COLORS[SHAPES.index(self.shape)]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2  # Center in play area
        self.y = 0

    def draw(self, surface):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.color,
                                     (GRID_X_OFFSET + (self.x + x) * BLOCK_SIZE, (self.y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)
    def move(self, dx, dy):
        if not check_collision(self.shape, (self.x + dx, self.y + dy)):
            self.x += dx
            self.y += dy

    def rotate(self):
        rotated_shape = rotate_shape(self.shape)
        if not check_collision(rotated_shape, (self.x, self.y)):
            self.shape = rotated_shape

    def drop_to_bottom(self):
        while not check_collision(self.shape, (self.x, self.y + 1)):
            self.y += 1
        self.lock_piece()

    def lock_piece(self):
        global current_tetrimino, hold_locked, fall_speed
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[self.y + y][self.x + x] = self.color
        clear_lines()

        # Dynamic fall speed based on score
        base_speed = 500
        speed_reduction = min(score // 25, 450)
        fall_speed = max(50, base_speed - speed_reduction)

        current_tetrimino = next_tetriminos.pop(0)
        next_tetriminos.append(Tetrimino())
        hold_locked = False
        if check_collision(current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y)):
            pygame.quit()


def draw_queue(surface):
    font = pygame.font.Font(None, 24)
    text = font.render("Next Pieces:", True, WHITE)
    surface.blit(text, (SCREEN_WIDTH - 140, 10))
    for i, piece in enumerate(next_tetriminos):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, piece.color,
                                     (SCREEN_WIDTH - 120 + x * BLOCK_SIZE, 40 + i * 80 + y * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)

def draw_hold(surface):
    pygame.draw.rect(surface, BLACK, (0, 0, GRID_X_OFFSET, SCREEN_HEIGHT))  # Black background for hold area

    font = pygame.font.Font(None, 24)
    text = font.render("Hold:", True, WHITE)
    surface.blit(text, (10, 10))  # Text label

    if hold_piece:
        for y, row in enumerate(hold_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, hold_piece.color,
                                     (30 + x * BLOCK_SIZE, 40 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def hold_current_piece():
    global current_tetrimino, hold_piece, hold_locked
    if hold_locked:
        return  # Prevent instant recall

    if hold_piece:
        hold_piece, current_tetrimino = current_tetrimino, hold_piece
    else:
        hold_piece = current_tetrimino
        current_tetrimino = next_tetriminos.pop(0)
        next_tetriminos.append(Tetrimino())

    hold_locked = True  # Prevent immediate recall
    current_tetrimino.x = (SCREEN_WIDTH // BLOCK_SIZE - 5) // 2 - len(current_tetrimino.shape[0]) // 2
    current_tetrimino.y = 0

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

next_tetriminos = [Tetrimino() for _ in range(3)]
current_tetrimino = Tetrimino()
hold_piece = None
hold_locked = False
fall_time = 0

running = True
while running:
    screen.fill(BLACK)
    draw_grid(screen)
    draw_queue(screen)
    draw_hold(screen)
    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
    current_tetrimino.draw(screen)
    pygame.display.flip()

    fall_time += clock.get_rawtime()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetrimino.move(-1, 0)
            if event.key == pygame.K_RIGHT:
                current_tetrimino.move(1, 0)
            if event.key == pygame.K_DOWN:
                current_tetrimino.move(0, 1)
            if event.key == pygame.K_UP:
                current_tetrimino.rotate()
            if event.key == pygame.K_SPACE:
                current_tetrimino.drop_to_bottom()
            if event.key == pygame.K_c:
                hold_current_piece()

    if fall_time > fall_speed:
        if not check_collision(current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y + 1)):
            current_tetrimino.y += 1
        else:
            current_tetrimino.lock_piece()
        fall_time = 0

pygame.quit()