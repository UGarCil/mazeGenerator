# implement a recursive approximation to the problem of modelling a maze.
# In V1 we implemented the backtracking algorithm to create a visual representation of a maze.

from tkinter.tix import CELL
import pygame
import random


def generateMaze(renderGrid=False, DIMS = (5,5),CELLSIZE = 16, FPS = 60):
    # GLOBAL VARIABLES
    global currentCell

    
    # :.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.
    # :.:.:.:.:.:.:.:.:. DATA DEFINITIONS :.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.

    # CELL
    class Cell():
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.xPos = x * CELLSIZE
            self.yPos = y * CELLSIZE
            self.walls = [True for t in range(4)]
            self.visited = False
            self.rect = pygame.Rect(self.xPos, self.yPos, CELLSIZE, CELLSIZE)
            # Variables for "forward backtracking"
            self.fdVisited = False
            self.solutionVisited = False


        def getColor(self):
            color = ""
            if self.visited and not self.fdVisited:
                color = "blue"
            elif self.fdVisited:
                color = 'green'
            elif self.solutionVisited:
                color = "gold"
            else:
                color = "#1e1e1e"
            return(color)

    # LIST-OF-CELL
    # loc = [CELL, ...]
    # interp. a list of cell
    loc = []
    for x in range(10):
        newCell = Cell(x, 0)
        loc.append(newCell)

    # GRID-OF-CELL
    # grid = [LIST-OF-CELL, ...]
    # interp. a 2d array of cells
    grid = []
    for y in range(DIMS[1]):
        loc = []
        for x in range(DIMS[0]):
            newCell = Cell(x, y)
            loc.append(newCell)
        grid.append(loc)

    # Variables required by pygame
    SCREEN = (DIMS[0]*CELLSIZE, DIMS[1]*CELLSIZE)
    display = pygame.display.set_mode(SCREEN)
    clock = pygame.time.Clock()

    # :.:.:.:.:.:.:.:.:.:.:.:.FUNCTIONS AND TEMPLATES:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.
    # Initialization variables
    stack = []
    currentCell = grid[0][0]
    stack.append(currentCell)
    currentCell.visited = True


    # FD. render()
    # Signature: None -> None
    # purp. draw the sides of each of the cells in the grid render images
    def render():
        display.fill("#1e1e1e")
        for row in grid:
            for cell in row:
                if not cell == currentCell:
                    pygame.draw.rect(display,cell.getColor(),cell.rect)
                else:
                    pygame.draw.rect(display,"red",cell.rect)



                if cell.walls[0]:
                    # draw right line at (x,y), (x + CELLSIZE,y)
                    pygame.draw.line(display, "#aaaaaa", (cell.xPos+CELLSIZE, cell.yPos),
                                    (cell.xPos + CELLSIZE, cell.yPos + CELLSIZE))
                if cell.walls[1]:
                    # draw bottom line at (x,y+CELLSIZE), (x+CELLSIZE,y+CELLSIZE)
                    pygame.draw.line(display, "#aaaaaa", (cell.xPos, cell.yPos +
                                                    CELLSIZE), (cell.xPos+CELLSIZE, cell.yPos+CELLSIZE))
                if cell.walls[2]:
                    # draw left line at (x,y), (x,y+CELLSIZE)
                    pygame.draw.line(display, "#aaaaaa", (cell.xPos, cell.yPos),
                                    (cell.xPos, cell.yPos+CELLSIZE))
                if cell.walls[3]:
                    # draw up line at (x,y), (x+CELLSIZE,y)
                    pygame.draw.line(display, "#aaaaaa", (cell.xPos, cell.yPos),
                                    (cell.xPos+CELLSIZE, cell.yPos))

        pygame.display.flip()
        clock.tick(FPS)

    # FD. userMan
    # Signature: None -> None
    # purp. receive and handle user' input
    def userMan():
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                pass


    # FD. getNeigh()
    # Signature: None -> None
    # purp. identify the neighbors that a cell has at any given time
    def getNeigh(cell):
        x = cell.x
        y = cell.y
        neighbors = []
        # RIGHT
        try:
            if not grid[y][x+1].visited:
                neighbors.append(grid[y][x+1])
        except:
            pass
        # DOWN
        try:
            if not grid[y+1][x].visited:
                neighbors.append(grid[y+1][x])
        except:
            pass
        # LEFT
        try:
            if not grid[y][x-1].visited and x>0:
                neighbors.append(grid[y][x-1])
        except:
            pass
        # UP
        try:
            if not grid[y-1][x].visited and y>0:
                neighbors.append(grid[y-1][x])
        except:
            pass

        return(neighbors)

    # FD. eraseWalls()
    # Signature: CELL -> None
    # purp. erase the walls and update the identity of the current cell
    def eraseWalls(cell):
        global currentCell
        # RIGHT
        if (currentCell.x - cell.x) == -1:
            currentCell.walls[0] = False
            cell.walls[2] = False
        # DOWN
        if (currentCell.y - cell.y) == -1:
            currentCell.walls[1] = False
            cell.walls[3] = False
        # LEFT
        if (currentCell.x - cell.x) == 1:
            currentCell.walls[2] = False
            cell.walls[0] = False
        # UP
        if (currentCell.y - cell.y) == 1:
            currentCell.walls[3] = False
            cell.walls[1] = False
        
        currentCell = cell

    # FD. update()
    # Signature: None -> None
    # purp. update the states of the cells and the walls in the maze
    def update():
        global currentCell
        # 1. determine the neighbors of the current cell
        neighbors = getNeigh(currentCell)
        # 2. select one the neighbors to be the new current cell and add it to the stack
        # otherwise, if the lenght of the stack is bigger than zero, make the current cell the last
        # element in the array stack
        if len(neighbors) > 0:
            chosenCell = random.choice(neighbors)
            chosenCell.visited = True
            stack.append(chosenCell)
            # 3. erase the walls in between the new current cell and the previous cell
            eraseWalls(chosenCell)
        else:
            if len(stack)>0:
                currentCell = stack[-1]
                stack.pop(-1)
        

    # run as long as there is something in the stack
    while len(stack)>0:
        if renderGrid:
            render()
        userMan()
        update()
    pygame.quit()
    return (grid)