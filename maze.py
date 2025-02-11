from drawables import Cell, Point, Circle, Text
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window, frametime, seed = None, animate_creation = False):
        """Initialised the maze object. x1, y1 are offsets from the top left
        of the frame, after which the maze is drawn. cell sizes are in pixels.
        The frametime, if non-zero, creates a stepped animation on render. The
        seed determines the path the maze creation algorithm takes."""

        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.frametime = frametime
        self.animate_creation = animate_creation
        self.dead_end_markers ={}
        if seed:
            random.seed(seed)
        else:
            random.seed(0)
        self.create_cells()

    def create_cells(self):
        """Creates cells according to the values set in __init__.
        stored them in a dict with keys representing the index of
        each cell in the overall maze grid. Then each cell is drawn."""

        self.cells = {(i,j):Cell(self.window,
                           Point(self.x1 + i * self.cell_size_x, self.y1 + j * self.cell_size_y),
                           Point(self.x1 + (i + 1) * self.cell_size_x, self.y1 +  (j + 1) * self.cell_size_y)) for i in range(self.num_cols) for j in range(self.num_rows)}

        if self.animate_creation:
            for cell in self.cells.values():
                self.draw_cell(cell, True)
        else:
            for cell in self.cells.values():
                self.draw_cell(cell)
    
    def draw_cell(self, cell, animation=False):
        cell.draw()
        self.animate(animation)
    
    def animate(self, animation = False):
        """Pauses before updating the canvas to allow the output
        to show the progressive development of the algorithm."""

        self.window.redraw()
        if animation:
            time.sleep(self.frametime)
    
    def break_entrance_and_exit(self):
        """removes the top edge of the top left cell, and the 
        bottom edge of the bottom left cell - in order that the 
        maze has an entry and exit point."""

        self.cells[(0,0)].remove_edge('u')
        self.cells[(self.num_cols-1, self.num_rows-1)].remove_edge('d')

    def get_unvisited_adjacent_cells(self, cell):
        """identifies all adjacent cells to a given cell,
        which are within the boundaries of the maze, and 
        which have not already been visited."""

        adjacents = {'l' : (cell[0] - 1, cell[1]), 
                     'd' : (cell[0], cell[1] + 1), 
                     'r' : (cell[0] + 1, cell[1]), 
                     'u' : (cell[0], cell[1] - 1)}
        valids = {}
        for direction, cell in adjacents.items():
            if cell in self.cells:
                if not self.cells[cell].visited:
                    valids[direction] = cell

        return valids

    def break_walls_recursively(self, current_cell):
        """Recursive backtracking algorithm to generate maze.
        Guarantees only one valid solution and all cells
        included in the maze (no loops)."""

        self.cells[current_cell].visited = True

        oppo = {'l':'r',
                'r':'l',
                'u':'d',
                'd':'u'}

        while True:
            adjacent_cells = self.get_unvisited_adjacent_cells(current_cell)
            if not adjacent_cells:
                # print()
                # print("no adjacent cells from current cell: ")
                # print(current_cell)
                return
            new_direction = random.choice(list(adjacent_cells.keys()))
            new_cell = adjacent_cells[new_direction]
            self.cells[current_cell].remove_edge(new_direction)
            self.cells[new_cell].remove_edge(oppo[new_direction])
            # debugging
            # print()
            # print("current step")
            # print("current cell")
            # print(current_cell)
            # print("valid adjacent cells")
            # print(adjacent_cells)
            # print("chosen next cell")
            # print(new_cell)
            self.animate()
            
            self.break_walls_recursively(new_cell)
    
    def reset_cells_visited(self):
        for cell in self.cells.values():
            cell.visited = False

    def defill_all_visited_cells(self):
        for cell in self.cells.values():
            if cell.visited:
                cell.remove_fill()

    def fill_all_unvisited_cells(self):
        for cell in self.cells.values():
            if not cell.visited:
                cell.fill()

    def get_unvisited_adjacent_cells_for_solve(self, current_cell):
        """identifies all adjacent cells to a given cell,
        which are within the boundaries of the maze, and 
        which have not already been visited."""

        adjacents = {'l' : (current_cell[0] - 1, current_cell[1]), 
                     'd' : (current_cell[0], current_cell[1] + 1), 
                     'r' : (current_cell[0] + 1, current_cell[1]), 
                     'u' : (current_cell[0], current_cell[1] - 1)}
        current_walls = {'l' : self.cells[current_cell].has_left,
                         'r' : self.cells[current_cell].has_right,
                         'u' : self.cells[current_cell].has_up,
                         'd' : self.cells[current_cell].has_down}
        
        valids = {}
        for direction, new_cell in adjacents.items():
            if new_cell in self.cells:
                if not self.cells[new_cell].visited:
                    if not current_walls[direction]:
                        valids[direction] = new_cell

        return valids

    def get_all_non_walled_adjacent_cells(self, current_cell):
        """identifies all adjacent cells to a given cell,
        which are within the boundaries of the maze."""

        adjacents = {'l' : (current_cell[0] - 1, current_cell[1]), 
                     'd' : (current_cell[0], current_cell[1] + 1), 
                     'r' : (current_cell[0] + 1, current_cell[1]), 
                     'u' : (current_cell[0], current_cell[1] - 1)}
        current_walls = {'l' : self.cells[current_cell].has_left,
                         'r' : self.cells[current_cell].has_right,
                         'u' : self.cells[current_cell].has_up,
                         'd' : self.cells[current_cell].has_down}
        
        valids = {}
        for direction, new_cell in adjacents.items():
            if new_cell in self.cells:
                if not current_walls[direction]:
                    valids[direction] = new_cell

        return valids

    def get_cells_neighbouring_over_wall(self, current_cell):
        """identifies all adjacent cells to a given cell,
        which are within the boundaries of the maze, and 
        which are across a wall from the current cell."""

        adjacents = {'l' : (current_cell[0] - 1, current_cell[1]), 
                     'd' : (current_cell[0], current_cell[1] + 1), 
                     'r' : (current_cell[0] + 1, current_cell[1]), 
                     'u' : (current_cell[0], current_cell[1] - 1)}
        current_walls = {'l' : self.cells[current_cell].has_left,
                         'r' : self.cells[current_cell].has_right,
                         'u' : self.cells[current_cell].has_up,
                         'd' : self.cells[current_cell].has_down}
        
        valids = {}
        for direction, new_cell in adjacents.items():
            if new_cell in self.cells:
                    if current_walls[direction]:
                        valids[direction] = new_cell

        return valids

    def break_additional_walls(self, number):
        oppo = {'l':'r',
                'r':'l',
                'u':'d',
                'd':'u'}
        chosen = random.choices(list(self.cells.keys()),k=number)
        for choice in chosen:
            cell = self.cells[choice]
            neighbours = self.get_cells_neighbouring_over_wall(choice)
            if neighbours:
                choice_pair = random.choice(list(neighbours.keys()))
                self.cells[choice].remove_edge(choice_pair)
                self.cells[neighbours[choice_pair]].remove_edge(oppo[choice_pair])

    def solve(self):
        # self.fill_all_unvisited_cells()
        if self.solve_recursive((0, 0)):
            self.defill_all_visited_cells()
            return True
        return False

    def solve_recursive(self, current_cell):
        
        current_marker_object = Circle(self.cells[current_cell].get_centre(), 5)
        current_marker = self.window.draw_circle(current_marker_object, "blue")
        
        self.defill_all_visited_cells()
        self.animate(True)
        
        self.cells[current_cell].visited = True
        if current_cell == (self.num_cols-1, self.num_rows-1):
            return True
        
        options = self.get_unvisited_adjacent_cells_for_solve(current_cell)

        # print(options)

        for direction, new_cell in options.items():

            self.window.delete_item(current_marker)
            self.cells[current_cell].draw_move(self.cells[new_cell])

            if self.solve_recursive(new_cell):
                return True
            self.cells[current_cell].draw_move(self.cells[new_cell], undo = True)

            retreating_marker_object = Circle(self.cells[current_cell].get_centre(), 5)
            retreating_marker = self.window.draw_circle(retreating_marker_object, "blue")

            self.animate(True)
            self.window.delete_item(retreating_marker)
        self.window.delete_item(current_marker)
        # try:
            
        # except NameError:
        #     print("no retreating marker to delete")

        return False
    
    def get_all_dead_end_cells(self, include_start_and_end):
        self.dead_ends = {}
        for key, cell in self.cells.items():
            if cell.is_dead_end():
                self.dead_ends[key] = cell
        
        if include_start_and_end:
            self.dead_ends[(0,0)] = self.cells[(0,0)]
            self.dead_ends[(self.num_cols-1, self.num_rows-1)] = self.cells[(self.num_cols-1, self.num_rows-1)] 


    def draw_dead_ends(self):
        for key, cell in self.dead_ends.items():
            dead_end = Circle(cell.get_centre(), 5)
            dead_end_marker = self.window.draw_circle(dead_end, "blue")

    def find_distance_to_nearest_dead_end(self, initial_cell):
        """Implement a breadth-first search for the nearest dead end.
        Returns the number of steps taken to reach the nearest dead end."""
        
        distance_travelled = 0

        if initial_cell in self.dead_ends:
            return distance_travelled

        to_visit = list(self.get_unvisited_adjacent_cells_for_solve(initial_cell).values())
        already_visited = [initial_cell]

        while True:
            to_visit_this_round = to_visit.copy()
            to_visit = []
            distance_travelled += 1
            for neighbouring_cell in to_visit_this_round:
                if neighbouring_cell in self.dead_ends:
                    return distance_travelled
                new_cells = self.get_unvisited_adjacent_cells_for_solve(neighbouring_cell).values()
                for identified_cell in new_cells:
                    if identified_cell not in already_visited and identified_cell not in to_visit:
                        to_visit.append(identified_cell)

        return 500
    
    def set_nearest_dead_ends(self):
        for cell in self.cells:
            result = self.find_distance_to_nearest_dead_end(cell)
            self.cells[cell].nearest_dead_end = result

    def draw_nearest_dead_ends(self):
        for key, cell in self.cells.items():
            #draw a text in each cell with the cell.distance_to_dead_end value
            centre = cell.get_centre()
            count = Text(centre.x, centre.y, text = cell.nearest_dead_end)
            self.dead_end_markers[key] = self.window.draw_text(count, "black")

    def is_cell_reachable(self, cell_1_inds, cell_2_inds):
        valids = self.get_all_non_walled_adjacent_cells(cell_1_inds)
        if cell_2_inds in valids.values():
            return True
        return False