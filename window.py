from tkinter import Tk, BOTH, Canvas

class Window:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.root_widget = Tk()
            self.title = "title"
            self.canvas = Canvas(self.root_widget, {"width": self.width, "height": self.height})
            self.canvas.pack()
            self.is_running = False
            self.root_widget.protocol("WM_DELETE_WINDOW", self.close)

        def redraw(self):
            self.root_widget.update_idletasks()
            self.root_widget.update()

        def wait_for_close(self):
            self.is_running = True
            while self.is_running:
                self.redraw()

        def close(self):
            self.is_running = False

        def draw_line(self, line, fill_colour):
            return line.draw(self.canvas, fill_colour)
        
        def delete_item(self, item):
            self.canvas.delete(item)

        def draw_circle(self, circle, fill_colour):
            return circle.draw(self.canvas, fill_colour)

        def fill_cell(self, cell):
            return self.canvas.create_rectangle(cell.top_left.x,
                                                cell.top_left.y,
                                                cell.bottom_right.x,
                                                cell.bottom_right.y,
                                                fill = "black")

