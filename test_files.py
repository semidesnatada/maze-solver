from drawables import Point, Line, Cell
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