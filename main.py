from window import Window
from drawables import Point, Line, Cell
from maze import Maze
import random

def draw_test_lines(window):
    factor = 50
    lines_1 = [Line(Point(factor*i, factor*j),
                    Point(factor*(i + 1), factor*(j + 1))) for i in range(7, 10) for j in range(4, 7)]
    lines_2 = [Line(Point(factor*(i+1), factor*j),
                    Point(factor*i, factor*(j + 1))) for i in range(7, 10) for j in range(4, 7)]

    for line in lines_1:
        window.draw_line(line, "black")
    for line in lines_2:
        window.draw_line(line, "red")   

def draw_test_cells(window):
    factor = 5
    cells = [Cell(window,
                  Point(factor * i, factor * i),
                  Point(factor * (i + 10), factor * (i + 10)),
                  left = random.choice([True, False]),
                  right = random.choice([True, False]),
                  up = random.choice([True, False]),
                  down = random.choice([True, False])
                  ) for i in range(7, 70, 2*factor)]
    
    # cells.append(Cell(window,Point(205, 600), Point(10, 12)))
    # cells[0].draw_move(cells[1])

    for cell in cells:
        cell.draw()

def draw_test_maze_large(window):

    maze = Maze(x1 = 50,
                y1 = 50,
                num_rows = 25,
                num_cols = 35,
                cell_size_x = 20,
                cell_size_y = 20,
                window = window,
                frametime = 0.1,
                seed = "sean-smells",
                animate_creation=False)

    maze.break_entrance_and_exit()
    maze.break_walls_recursively((0,0))
    maze.reset_cells_visited()
    maze.solve()

def draw_test_maze_medium(window):

    maze = Maze(x1 = 50,
                y1 = 50,
                num_rows = 10,
                num_cols = 14,
                cell_size_x = 50,
                cell_size_y = 50,
                window = window,
                frametime = 0.2,
                seed = "veronica-smells",
                animate_creation=False)

    maze.break_entrance_and_exit()
    maze.break_walls_recursively((0,0))
    maze.reset_cells_visited()
    maze.solve()

def draw_test_maze_small(window):

    maze = Maze(x1 = 50,
                y1 = 50,
                num_rows = 5,
                num_cols = 7,
                cell_size_x = 100,
                cell_size_y = 100,
                window = window,
                frametime = 0.005,
                animate_creation=True)

    maze.break_entrance_and_exit()
    maze.break_walls_recursively((0,0))
    maze.reset_cells_visited()
    maze.solve()


def main():

    win = Window(800, 600)

    # draw_test_lines(win)
    # draw_test_cells(win)
    draw_test_maze_small(win)

    win.wait_for_close()
    print("hello world")

if __name__ == "__main__":
    main()
