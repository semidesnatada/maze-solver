# maze-solver

A tool which generates a maze of a given size, using the recursive backtracking algorithm.

This maze can then be solved using a depth-first search if desired - the progress of this algorithm can be visualised.

There are also options for interactivity and self-solving. The current main.py file when run from terminal should yield a large maze which you can solve by yourself.

Latest new functionality includes:
* option for destruction of additional walls within the maze, to provide more choice for the player. while this means the maze is no longer a "perfect maze" (as perfect mazes have only one solution) this reduces the ability of the player to quickly identify when they have deviated from the solution path.
* an integer value to each cell, which is drawn to the window, which represents the distance of that cell from a dead end (the maze start and end cells are also considered dead ends). This is calculated using a breadth-first algorithm.
* a player score which counts down by the value of the above integer value upon entering a cell.
* logic which only allows the player to make valid moves (though backtracking is permitted).
* ability to hide unvisited cells from view (so only explored parts of the maze are visible in the render).

The current code requires further improvement in a number of areas:
- the rendering and game logic are currently highly coupled. This is useful for the purposes of rendering an animated view of the progression of the maze creation and solve algorithms, but is less clean.
- there is plenty duplication across the Maze methods, which should be simplified.
- properties of the various classes should be refactored to more sensible areas. currently, they only sit where was most convenient upon creation.

This code may be extended further:
- To provide GUI indication of player score.
- To provide buttons with options for showing the shortest path to the solution, resetting progress, regenerating the maze, etc.
- Powerups for the interactive game section (e.g. spend points to gain additional visibility, or to see a section of the shortest path).
- Choice of start point (which then allocates an end point a sufficient distance away.
- Handling of maze construction in GUI, as opposed to in main.py.
