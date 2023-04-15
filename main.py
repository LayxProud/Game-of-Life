import pygame
import numpy as np

# Set up the Pygame display
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Set up the grid
CELL_SIZE = 10
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)

# Function to draw the grid on the Pygame display
def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == 1:
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (255, 255, 255), rect)

# Function to get the indices of neighboring cells
def get_neighbors(x, y):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbors.append(((x+i) % GRID_WIDTH, (y+j) % GRID_HEIGHT))
    return neighbors

# Function to update the grid for one step
def update_grid():
    new_grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            num_neighbors = sum([grid[nx][ny] for nx, ny in get_neighbors(x, y)])
            if grid[x][y] == 1:
                if num_neighbors in [2, 3]:
                    new_grid[x][y] = 1
            else:
                if num_neighbors == 3:
                    new_grid[x][y] = 1
    return new_grid

# Main game loop
running = True
paused = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x //= CELL_SIZE
            y //= CELL_SIZE
            grid[x][y] = 1

    # Update the grid
    if not paused:
        grid = update_grid()

    # Clear the screen and draw the grid
    screen.fill((0, 0, 0))
    draw_grid()

    # Update the Pygame display
    pygame.display.flip()

# Quit Pygame
pygame.quit()