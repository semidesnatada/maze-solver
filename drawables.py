class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x, self.y})"

class Text:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw(self, canvas, fill_colour):
        return canvas.create_text(self.x,
                                  self.y, 
                                  fill = fill_colour,
                                  text = self.text)

class Circle:
    def __init__(self, centre, r):
        self.centre = centre
        self.r = r
    
    def draw(self, canvas, fill_colour):
        return canvas.create_oval(self.centre.x-self.r,
                                  self.centre.y-self.r,
                                  self.centre.x+self.r,
                                  self.centre.y+self.r, 
                                  fill = fill_colour)

class Player(Circle):
    def __init__(self, index_location, centre, r):
        super().__init__(centre, r)
        self.index_location = index_location
        self.score = 200

    def draw(self, canvas):
        return canvas.create_oval(self.centre.x-self.r,
                                  self.centre.y-self.r,
                                  self.centre.x+self.r,
                                  self.centre.y+self.r, 
                                  fill = "orange")


class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, canvas, fill_colour):
       return canvas.create_line(self.point_1.x,
                                 self.point_1.y,
                                 self.point_2.x,
                                 self.point_2.y,
                                 fill = fill_colour,
                                 width = 2)

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
        self.filled = False
        self.reorganise_corners()
        self.check_corners_are_valid()

    def __repr__(self):
        return f"Cell(top-left:{self.top_left}, bottom-right:{self.bottom_right}, walls: left({self.has_left}), right({self.has_right}), top({self.has_up}), bottom({self.has_down}). visited = {self.visited})"

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

    def fill(self):
        self.filled = self.window.fill_cell(self)
    
    def remove_fill(self):
        self.window.delete_item(self.filled)

    def draw(self):
        if self.has_left:
            self.edges_drawn['l'] = self.window.draw_line(Line(self.top_left, Point(self.top_left.x, self.bottom_right.y)), "black")
        if self.has_right:
            self.edges_drawn['r'] = self.window.draw_line(Line(self.bottom_right, Point(self.bottom_right.x, self.top_left.y)), "black")
        if self.has_up:
            self.edges_drawn['u'] = self.window.draw_line(Line(self.top_left, Point(self.bottom_right.x, self.top_left.y)), "black")
        if self.has_down:
            self.edges_drawn['d'] = self.window.draw_line(Line(self.bottom_right, Point(self.top_left.x, self.bottom_right.y)), "black")
    
    def get_centre(self):
        return Point((self.top_left.x + self.bottom_right.x) / 2, (self.top_left.y + self.bottom_right.y) / 2)

    def draw_move(self, other, undo=False):
        connection = Line(self.get_centre(), other.get_centre())
        if undo:
            self.window.draw_line(connection, "gray")
        else:
            self.window.draw_line(connection, "red")
    
    def remove_edge(self, side):
        self.window.delete_item(self.edges_drawn[side])
        if side == "l":
            self.has_left = False
        elif side == "r":
            self.has_right = False
        elif side == 'u':
            self.has_up = False
        else:
            self.has_down = False
    
    def is_dead_end(self):
        num_sides = [self.has_left, self.has_right, self.has_up, self.has_down].count(True)
        if num_sides == 3:
            return True
        return False
