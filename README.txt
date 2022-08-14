Maze generation with translation to ASCII

Produce a maze, then increase the dimensionality of the array to allocate new cells for each of the walls.
1. Duplicate the dimensions of a given grid
2. For each cell in the grid, fill with an O
3. If a cell has a given wall filled with a line (wall), then place an X to the direction of that neighbor relative to the position of the cell
4. Return the maze as a list of strings