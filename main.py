import pygame
import numpy as np
import time

# Set up the Pygame display
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Set the initial zoom level
CELL_SIZE = 10
MIN_CELL_SIZE = 1
MAX_CELL_SIZE = 100
VIEW_SPEED = 0.25

# Set the grid
GRID_WIDTH = 800 
GRID_HEIGHT = 600
grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)

# Set up the initial view
view_x = GRID_WIDTH // 2 - SCREEN_WIDTH // (2 * CELL_SIZE)
view_y = GRID_HEIGHT // 2 - SCREEN_HEIGHT // (2 * CELL_SIZE)

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
    # Compute the number of live neighbors for each cell
    num_neighbors = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            num_neighbors += np.roll(grid, (i, j), axis=(0, 1))

    # Apply the Game of Life rules to compute the next state
    new_grid = np.logical_or(
        np.logical_and(grid, num_neighbors == 2),
        num_neighbors == 3
    )

    return new_grid

# Main game loop
running = True
paused = True
drawing = False
erasing = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Handle quitting the game
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Handle pausing the game
                paused = not paused

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                # Handle drawing cells
                drawing = True
            elif event.button == pygame.BUTTON_RIGHT:
                # Handle erasing cells
                erasing = True
                x, y = pygame.mouse.get_pos()
                grid_x = (x // CELL_SIZE) + view_x
                grid_y = (y // CELL_SIZE) + view_y
                grid[grid_x][grid_y] = 0
            elif event.button == pygame.BUTTON_WHEELUP:
                # Handle mouse wheel up to zoom in
                old_cell_size = CELL_SIZE
                CELL_SIZE = min(MAX_CELL_SIZE, CELL_SIZE + 1)
                dx = ((SCREEN_WIDTH // old_cell_size) - (SCREEN_WIDTH // CELL_SIZE)) // 2
                dy = ((SCREEN_HEIGHT // old_cell_size) - (SCREEN_HEIGHT // CELL_SIZE)) // 2
                view_x += dx
                view_y += dy
            elif event.button == pygame.BUTTON_WHEELDOWN:
                # Handle mouse wheel down to zoom out
                old_cell_size = CELL_SIZE
                CELL_SIZE = max(MIN_CELL_SIZE, CELL_SIZE - 1)
                grid_center_x = GRID_WIDTH // 2
                grid_center_y = GRID_HEIGHT // 2
                view_x = grid_center_x - (SCREEN_WIDTH // (2 * CELL_SIZE))
                view_y = grid_center_y - (SCREEN_HEIGHT // (2 * CELL_SIZE))
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                drawing = False
            elif event.button == pygame.BUTTON_RIGHT:
                erasing = False
            
    # Update the view position based on the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        view_x -= VIEW_SPEED
    if keys[pygame.K_RIGHT]:
        view_x += VIEW_SPEED
    if keys[pygame.K_UP]:
        view_y -= VIEW_SPEED
    if keys[pygame.K_DOWN]:
        view_y += VIEW_SPEED

    # Update the grid
    if not paused:
        grid = update_grid()
        time.sleep(0.001)

    # Draw cells when the left mouse button is pressed
    if drawing:
        x, y = pygame.mouse.get_pos()
        grid_x = (x // CELL_SIZE) + view_x
        grid_y = (y // CELL_SIZE) + view_y
        grid[grid_x][grid_y] = 1

    # Erase cells when the right mouse button is pressed
    if erasing:
        x, y = pygame.mouse.get_pos()
        grid_x = (x // CELL_SIZE) + view_x
        grid_y = (y // CELL_SIZE) + view_y
        grid[grid_x][grid_y] = 0

    # Clear the screen and draw the cells
    screen.fill((0, 0, 0))
    cells = np.argwhere(grid)
    for cell in cells:
        screen_x = (cell[0] - view_x) * CELL_SIZE
        screen_y = (cell[1] - view_y) * CELL_SIZE
        rect = pygame.Rect(screen_x, screen_y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 255, 255), rect)

    # Update the Pygame display
    pygame.display.flip()

# Quit Pygame
pygame.quit()