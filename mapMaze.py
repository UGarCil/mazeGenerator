# In V2 we use the states of the cell to implement backtracking again, this time in the effort of 
# solving the maze.
# To solve the maze we start with a grid of Cell() where each cell has an array of booleans, identifying the
# wall that are collapsed.
# Create an agent that moves from the tile 0,0 in a random walk, where the agent keeps track of the tiles seen
# and never goes back to one tile it already saw

# IMPORTS
from mazeGenerator import *
import pygame
import random

# :.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.DATA DEFINITIONS:.:.:.:.:.:.:.:.:.:.:.:.:.

# DD. GRID
# grid = generateMaze(bool)
# interp. a grid of Cell() with walls collapsed, representing a maze
# grid = generateMaze(True)  #a maze of 20,20

# FD. mapMaze()
# Signature: GRID -> MAP
def mapMaze(grid):

    # DD. 2GRID
    # grid2 = [str,...]
    # interp. a grid where the walls have been expanded to entire tiles
    # Restricted to X or O for wall and empty respectively
    rows2 = len(grid) * 2
    cols2 = len(grid[0]) * 2

    grid2 = [["X" for x in range(cols2)] for y in range(rows2)]


    for r,row in enumerate(grid):
        for c,tile in enumerate(row):
            # map the walls of the tile (bool) to each of the neighbors, handling the edges with try
            # RIGHT
            r2 = r*2
            c2 = c*2
            grid2[r2][c2] = "O"
            # RIGHT
            try:
                if tile.walls[0]:
                    grid2[r2][c2+1] = "X"
                else:
                    grid2[r2][c2+1] = "O"
            except:
                pass
            # DOWN
            try:
                if tile.walls[1]:
                    grid2[r2+1][c2] = "X"
                else:
                    grid2[r2+1][c2] = "O"
            except:
                pass
            # LEFT
            try:
                if c2>0:
                    if tile.walls[2]:
                        grid2[r2][c2-1] = "X"
                    else:
                        grid2[r2][c2-1] = "O"
            except:
                pass
            # UP
            try:
                if r2>0:
                    if tile.walls[3]:
                        grid2[r2-1][c2] = "X"
                    else:
                        grid2[r2-1][c2] = "O"
            except:
                pass


    # Create a list of str from grid2
    map = []
    strRow = ["X" for x in range(len(grid2[0])+1)]
    map.append(strRow)
    for row in grid2:
        strRow = "X" + "".join(row) + "X"
        map.append(strRow)
    map[1] = "O"+map[1][1:]
    map[-2] = map[-2][:-2] + "O"

    return(map)



