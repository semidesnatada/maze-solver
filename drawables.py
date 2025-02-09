class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x, self.y})"

class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, canvas, fill_colour):
       return canvas.create_line(self.point_1.x, self.point_1.y,self.point_2.x, self.point_2.y,fill = fill_colour, width = 2)

    def __eq__(self, other):
        comp_1 = self.point_1 == other.point_1 and self.point_2 == other.point_2
        comp_2 = self.point_1 == other.point_2 and self.point_2 == other.point_1
        return comp_1 or comp_2

    def __repr__(self):
        return f"Line(starts at {self.point_1}, ends at {self.point_2})"

class Cell:
    def __init__(self, window, top_left, bottom_right, left = True, right = True, up = True, down = True):
        self.has_left = left
        self.has_right = right
        self.has_up = up
        self.has_down = down
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.window = window
        self.edges_drawn = {}
        self.visited = False
        self.reorganise_corners()
        self.check_corners_are_valid()

    def __repr__(self):
        return f"Cell(top-left:{self.top_left}, bottom-right:{self.bottom_right}, walls: left({self.has_left}), right({self.has_right}), top({self.has_up}), bottom({self.has_down}))"

    def check_corners_are_valid(self):
        if self.top_left.x - self.bottom_right.x >= 0:
            raise Exception("cell corners do not produce a valid cell (x coords)")
        if self.top_left.y - self.bottom_right.y >= 0:
            raise Exception("cell corners do not produce a valid cell (y coords)")

    def reorganise_corners(self):
        if self.top_left.x > self.bottom_right.x or self.top_left.y > self.bottom_right.y:
            temp = self.top_left
            self.top_left = self.bottom_right
            self.bottom_right = temp

    def draw(self):
        if self.has_left:
            self.edges_drawn['l'] = self.window.draw_line(Line(self.top_left, Point(self.top_left.x, self.bottom_right.y)), "orange")
        if self.has_right:
            self.edges_drawn['r'] = self.window.draw_line(Line(self.bottom_right, Point(self.bottom_right.x, self.top_left.y)), "blue")
        if self.has_up:
            self.edges_drawn['u'] = self.window.draw_line(Line(self.top_left, Point(self.bottom_right.x, self.top_left.y)), "yellow")
        if self.has_down:
            self.edges_drawn['d'] = self.window.draw_line(Line(self.bottom_right, Point(self.top_left.x, self.bottom_right.y)), "black")
    
    def get_centre(self):
        return Point((self.top_left.x + self.bottom_right.x) / 2, (self.top_left.y + self.bottom_right.y) / 2)

    def draw_move(self, other, undo=False):
        connection = Line(self.get_centre(), other.get_centre())
        print()
        print(connection)
        print()
        if undo:
            self.window.draw_line(connection, "gray")
        else:
            self.window.draw_line(connection, "red")
    
    def remove_edge(self, side):
        self.window.delete_item(self.edges_drawn[side])
