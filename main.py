from pickle import POP
from re import T
import pygame
from mapMaze import mapMaze as mapMaze
from mazeGenerator import generateMaze as generateMaze
import random 

# Generate a maze using recursive backtracker and map the output into an array of strings to be mapped into tiles 

# :.:.:.:.:.:.:. DATA DEFINITIONS :.:.:.:.:.:.:.:.:.:.:.:.:.:.
POPULATION = 500
DIMS = (80,40)  #The dimensions of the final maze will be twice as big as these values for x and y
# DIMS = (10,10)
RES = 8
FPS = 30
TILESETNAME = "tileset"
# DD. CHAR
# char = str
# interp. a wall or empty space for the position of a tile in a maze. Is one of:
# - O   empty
# - X   wall
char_X = "X"
char_Y = "Y"

# DD. CHARROW
# charRow = [CHAR,...]
# interp. a string of CHAR representing a row of a maze
charRow0 = "XOX"
charRow1 = "XOX"
charRow2 = "XOO"

# DD. MAP
# map = [CHARROW, ...]
# interp. a list of rows to make a 2D array of a maze
map0 = []
map1 = [charRow0, charRow1, charRow2]
map2 = mapMaze(generateMaze(DIMS=DIMS))

# DD. TILE
# tile = Tile()
# interp. a tile in the map
class Tile():
    def __init__(self,x,y,char):
        self.xCoor = x
        self.yCoor = y
        self.x = x * RES
        self.y = y * RES
        self.char = char
        self.updateImage()

    def updateImage(self):
        if self.char == "X":
            self.image = pygame.image.load(f"./images/{TILESETNAME}/res_{RES}/{RES}_fill.png")
        else:
            self.image = pygame.image.load(f"./images/{TILESETNAME}/res_{RES}/{RES}_empty.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x,self.y

# DD. TILEGRID
# tileGrid = [[Tile(), ...]]
# interp. a grid of tiles mapped from a reference MAP of strings
tileGrid0 = []
tileGrid1 = [[Tile(0,0,"X"),Tile(1,0,"O"),Tile(2,0,"X")],\
             [Tile(0,1,"X"),Tile(1,1,"O"),Tile(2,1,"X")],\
             [Tile(0,2,"X"),Tile(1,2,"O"),Tile(2,2,"O")]  ]

tileGrid2 = []
for y,row in enumerate(map2):
    tileRow = []
    for x,char in enumerate(row):
        newTile = Tile(x,y,char)
        tileRow.append(newTile)
    tileGrid2.append(tileRow)

# DD. AGENT
# agent = Agent()
# interp. an element in the maze to solve the maze
class Agent():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.visitedTiles = []
        self.stack = []
        self.distance = 0
        self.agentStop = False
        self.goalReached = False
        self.moves = [{"IDX":x, "VALID":False} for x in range(4)]
        self.nextMove = 0
        self.updateRect()

    def updateRect(self):
        self.xPos = self.x * RES
        self.yPos = self.y * RES
        self.image = pygame.image.load(f"./images/{TILESETNAME}/res_{RES}/{RES}_agent.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.xPos, self.yPos)

    # FD updateAgentMoves()
    # Signature: None -> None
    # purp. update the possible movements that an agent can take in the enxt generation
    def updateAgentMoves(self):
        self.moves = [{"IDX":x, "VALID":False} for x in range(4)]
        # self.visitedTiles.append(grid[self.y][self.x])
        # RIGHT
        try:
            if grid[self.y][self.x + 1] not in self.visitedTiles and grid[self.y][self.x + 1].char == "O":
                self.moves[0]["VALID"] = True
        except:
            self.moves[0]["VALID"] = False
        # DOWN
        try:
            if grid[self.y + 1][self.x] not in self.visitedTiles and grid[self.y+1][self.x].char == "O":
                self.moves[1]["VALID"] = True
        except:
            self.moves[1]["VALID"] = False
        # LEFT
        try:
            if grid[self.y][self.x - 1] not in self.visitedTiles and self.x > 0 and grid[self.y][self.x-1].char == "O":
                self.moves[2]["VALID"] = True
        except:
            self.moves[2]["VALID"] = False
        # UP
        try:
            if grid[self.y -1][self.x] not in self.visitedTiles and self.y > 0 and grid[self.y-1][self.x].char == "O":
                self.moves[3]["VALID"] = True
        except:
            self.moves[3]["VALID"] = False

    # FD. moveAgents()
    # Signature: None -> None
    # purp. apply the agent's next move
    def moveAgents(self):
        if self.nextMove == 0: 
            self.x += 1
            
        if self.nextMove == 1:
            self.y += 1
            
        if self.nextMove == 2:
            self.x -= 1
            
        if self.nextMove == 3:
            self.y -= 1
        
        # Add the new tile visited to the stack and make it visited
        self.stack.append(grid[self.y][self.x])
        self.visitedTiles.append(grid[self.y][self.x])

    # FD. getAgentNextMove()
    # Signature: None -> None
    # purp. get hte agent's next move
    def getAgentNextMove(self):
        lopotMoves = []
        for potMove in self.moves:
            if potMove["VALID"]:
                lopotMoves.append(potMove["IDX"])

        if len(lopotMoves)>0:
            self.nextMove = random.choice(lopotMoves)
            self.moveAgents()
        else:
            if len(self.stack)>0:
                self.x = self.stack[-1].xCoor
                self.y = self.stack[-1].yCoor
                self.stack.pop(-1)
        self.updateRect()

agent = Agent(0,1)

# DD. LOAGENT
# loag = [Agent(),...]
# interp. a list of agents to move across the maze
loag = [Agent(0,1) for a in range(POPULATION)]

# CODE #####################################################################
grid = tileGrid2

# Variables required by pygame
SCREEN = (len(grid[0]) * RES,len(grid) * RES)
screen = pygame.display.set_mode(SCREEN)
clock = pygame.time.Clock()

# FD. draw()
# Signature: None -> None
# purp. render the elements in the SCREEN
def draw():
    for row in grid:
        for tile in row:
            screen.blit(tile.image, tile.rect)
    for agent in loag:
        screen.blit(agent.image, agent.rect)
    pygame.display.flip()
    clock.tick(FPS)

# FD. userMan()
# Signature: None-> None
# purp. handle the input system
def userMan():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()







# FD. update()
# Signature: None -> None
# purp. apply the changes to the generations of agents in the system
def update():
    # handle the user's input
    userMan()
    for agent in loag:
        if not agent.agentStop:
            # for each of the agents, evaluate the possible next moves
            agent.updateAgentMoves()
            # for each agent in loag, randomly choose a next direction.
            # if no directions left for a given agent, then make stop updating it
            agent.getAgentNextMove()
            # moveAgents()
            # When all agents have stopped, move to the next generation. The criterion of optimality in the system is how
            # close they have made it to the bottom right edge of the system. If an gent reches the tile -1,-2, it overwrites the system
            if agent.y == len(grid)-2 and agent.x == len(grid[0])-1:
                agent.agentStop = True

    # Once an agent has made it trhough the maze, run the animation one more time, this time following the directions
    # from that single agent that made it to the end

while True:
    draw()
    update()
