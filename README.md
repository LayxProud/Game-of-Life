# Description

A simple implementation of Conway's Game of Life. The goal of this task was to build a game on an infinite field, using functional programming paradigm. 

# Requirements

To build and run the game, pygame and numpy libs should be installed.

# Modifying the code

* To increase size of the window, *SCREEN_WIDTH* and *SCREEN_HEIGHT* variables should be modified (800x600 as default).
* To increase size of the grid, *GRID_WIDTH* and *GRID_HEIGHT* variables should be modified (800x600 as default). If grid is larger than the screen, objects will be out of bounds for a longer time. For better experience this variables should be tied to *SCREEN_WIDTH* and *SCREEN_HEIGHT* respectively. 
* *CELL_SIZE* variable defines the size of the cell in the beginning of the game. 
* *MIN_CELL_SIZE* variable defines the minimum size of the cell in the beginning of the game.
* *MAX_CELL_SIZE* variable defines the maximum size of the cell in the beginning of the game.
* *VIEW_SPEED* variable defines how fast the player can move around the field with arrow keys.
