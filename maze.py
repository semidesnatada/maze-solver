from drawables import Cell, Point, Line
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window, frametime, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.frametime = frametime
        if seed:
            random.seed(seed)
        else:
            random.seed(0)
        self.create_cells()


    def create_cells(self):
        self.cells = {(i,j):Cell(self.window,
                           Point(self.x1 + i * self.cell_size_x, self.y1 + j * self.cell_size_y),
                           Point(self.x1 + (i + 1) * self.cell_size_x, self.y1 +  (j + 1) * self.cell_size_y)) for i in range(self.num_cols) for j in range(self.num_rows)}

        for cell in self.cells.values():
            self.draw_cell(cell)
    
    def draw_cell(self, cell):
        cell.draw()
        self.animate()
    
    def animate(self):
        self.window.redraw()
        time.sleep(self.frametime)
    
    def break_entrance_and_exit(self):
        self.cells[(0,0)].remove_edge('u')
        self.cells[(self.num_cols-1, self.num_rows-1)].remove_edge('d')

    def get_unvisited_adjacent_cells(self, cell):

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
    