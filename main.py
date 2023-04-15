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
GRID_WIDTH = 200  # Set a fixed width and height for the grid
GRID_HEIGHT = 200
grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)

# Set up the initial view
view_x = 0
view_y = 0

# Function to draw the grid on the Pygame display
def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == 1:
                screen_x = (x - view_x) * CELL_SIZE
                screen_y = (y - view_y) * CELL_SIZE
                rect = pygame.Rect(screen_x, screen_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (255, 255, 255), rect)

# Function to get the indices of neighboring cells
def get_neighbors(x, y):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx = (x+i) % GRID_WIDTH
            ny = (y+j) % GRID_HEIGHT
            neighbors.append((nx, ny))
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
            elif event.key == pygame.K_LEFT:
                view_x -= 1
            elif event.key == pygame.K_RIGHT:
                view_x += 1
            elif event.key == pygame.K_UP:
                view_y -= 1
            elif event.key == pygame.K_DOWN:
                view_y += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x = (x // CELL_SIZE) + view_x
            grid_y = (y // CELL_SIZE) + view_y
            grid[grid_x][grid_y] = 1

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