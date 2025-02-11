
from mazetools import generate_and_solve_maze, generate_maze, set_up_playing_maze
from window import Window
from drawables import Player, Point

def main():

    window = Window(800, 600)
    maze = set_up_playing_maze(window, 'l')

    origin = list(maze.cells.values())[0].get_centre()

    maze.player = Player((0,0), origin, 10)
    maze.player_counter = window.draw_player(maze.player)
    make_interactive = True

    def move_down(event):
        new_index = maze.player.index_location
        new_index = (new_index[0], new_index[1]+1)
        if maze.is_cell_reachable(maze.player.index_location, new_index):
            maze.player.index_location = new_index
            maze.player.centre.y += maze.cell_size_y
            maze.player_counter = window.update_player(maze.player_counter, maze.player)
            print("Moving Down")
        else:
            print("Down is not a valid move")

    def move_up(event):
        new_index = maze.player.index_location
        new_index = (new_index[0], new_index[1]-1)
        if maze.is_cell_reachable(maze.player.index_location, new_index):
            maze.player.index_location = new_index
            maze.player.centre.y -= maze.cell_size_y
            maze.player_counter = window.update_player(maze.player_counter, maze.player)
            print("Moving Up")
        else:
            print("Up is not a valid move")
    
    def move_left(event):
        new_index = maze.player.index_location
        new_index = (new_index[0]-1, new_index[1])
        if maze.is_cell_reachable(maze.player.index_location, new_index):
            maze.player.index_location = new_index
            maze.player.centre.x -= maze.cell_size_x
            maze.player_counter = window.update_player(maze.player_counter, maze.player)
            print("Moving Left")
        else:
            print("Left is not a valid move")
    
    def move_right(event):
        new_index = maze.player.index_location
        new_index = (new_index[0]+1, new_index[1])
        if maze.is_cell_reachable(maze.player.index_location, new_index):
            maze.player.index_location = new_index
            maze.player.centre.x += maze.cell_size_x
            maze.player_counter = window.update_player(maze.player_counter, maze.player)
            print("Moving Right")
        else:
            print("Right is not a valid move")

    # make interactive
    if make_interactive:

        window.root_widget.bind("<Up>", lambda event: move_up(event))
        window.root_widget.bind("<Down>", lambda event: move_down(event))
        window.root_widget.bind("<Left>", lambda event: move_left(event))
        window.root_widget.bind("<Right>", lambda event: move_right(event))
        window.root_widget.mainloop()
    
    window.wait_for_close()
    print("hello world")

if __name__ == "__main__":
    main()
