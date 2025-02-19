from maze import Maze
from drawables import Player

def small_maze(window):
    small = Maze(x1 = 50,
                y1 = 50,
                num_rows = 5,
                num_cols = 7,
                cell_size_x = 100,
                cell_size_y = 100,
                window = window,
                frametime = 0.005,
                animate_creation=True)
    return small

def medium_maze(window):
    medium = Maze(x1 = 50,
                y1 = 50,
                num_rows = 10,
                num_cols = 14,
                cell_size_x = 50,
                cell_size_y = 50,
                window = window,
                frametime = 0.2,
                seed = "veronica-smells",
                animate_creation=False)
    return medium

def large_maze(window):
    large = Maze(x1 = 50,
                y1 = 50,
                num_rows = 25,
                num_cols = 35,
                cell_size_x = 20,
                cell_size_y = 20,
                window = window,
                frametime = 0.01,
                seed = "sean-smells",
                animate_creation=False)
    return large

def extra_large_maze(window):
    extra_large = Maze(x1 = 50,
                        y1 = 50,
                        num_rows = 35,
                        num_cols = 50,
                        cell_size_x = 14,
                        cell_size_y = 14,
                        window = window,
                        frametime = 0.00005,
                        seed = "beans",
                        animate_creation=True)
    return extra_large

def generate_and_solve_maze(window, size):
    if size == "s":        
        maze = small_maze(window)
    elif size == "m":
        maze = medium_maze(window)
    elif size == "l":
        maze = large_maze(window)
    elif size == "xl":
        maze = extra_large_maze(window)
    else:
        raise Exception("not a valid maze size")

    maze.break_entrance_and_exit()
    maze.break_walls_recursively((0,0))
    maze.reset_cells_visited()
    maze.solve()

def generate_maze(window, size, additional_walls):
    if size == "s":        
        maze = small_maze(window)
    elif size == "m":
        maze = medium_maze(window)
    elif size == "l":
        maze = large_maze(window)
    elif size == "xl":
        maze = extra_large_maze(window)
    else:
        raise Exception("not a valid maze size")

    maze.break_entrance_and_exit()
    maze.break_walls_recursively((0,0))
    maze.reset_cells_visited()

    if additional_walls:
        if size == "s":
            #good for a small maze
            maze.break_additional_walls(10)
        if size == "l":
            #good for a large maze
            maze.break_additional_walls(50)
        else:
            maze.break_additional_walls(20)

    # print(maze.find_distance_to_nearest_dead_end((0,1)))

    return maze

def set_up_playing_maze(window, size):
    maze = generate_maze(window, size, additional_walls=True)

    maze.get_all_dead_end_cells(include_start_and_end=True)
    # maze.draw_dead_ends()
    maze.set_nearest_dead_ends()
    maze.draw_dead_ends()
    maze.draw_nearest_dead_ends()

    return maze
    # maze.solve()

def make_interactive(maze, window):

    origin = list(maze.cells.values())[0].get_centre()

    maze.player = Player((0,0), origin, 10)
    maze.player_counter = window.draw_player(maze.player)

    def move_down(event):
        new_index = maze.player.index_location
        new_index = (new_index[0], new_index[1]+1)
        if maze.is_cell_reachable(maze.player.index_location, new_index):
            maze.player.index_location = new_index
            maze.player.centre.y += maze.cell_size_y
            maze.player_counter = window.update_player(maze.player_counter, maze.player)
            maze.player.score -= maze.cells[new_index].nearest_dead_end
            maze.cells[new_index].nearest_dead_end = 0
            window.delete_item(maze.dead_end_markers[new_index])
            print(f"Moving Down. Player score now {maze.player.score}")
        else:
            print("Down is not a valid move")

    def move_up(event):
        new_index = maze.player.index_location
        new_index = (new_index[0], new_index[1]-1)
        if maze.is_cell_reachable(maze.player.index_location, new_index):
            maze.player.index_location = new_index
            maze.player.centre.y -= maze.cell_size_y
            maze.player_counter = window.update_player(maze.player_counter, maze.player)
            maze.player.score -= maze.cells[new_index].nearest_dead_end
            maze.cells[new_index].nearest_dead_end = 0
            window.delete_item(maze.dead_end_markers[new_index])
            print(f"Moving Up. Player score now {maze.player.score}")
        else:
            print("Up is not a valid move")
    
    def move_left(event):
        new_index = maze.player.index_location
        new_index = (new_index[0]-1, new_index[1])
        if maze.is_cell_reachable(maze.player.index_location, new_index):
            maze.player.index_location = new_index
            maze.player.centre.x -= maze.cell_size_x
            maze.player_counter = window.update_player(maze.player_counter, maze.player)
            maze.player.score -= maze.cells[new_index].nearest_dead_end
            maze.cells[new_index].nearest_dead_end = 0
            window.delete_item(maze.dead_end_markers[new_index])
            print(f"Moving Left. Player score now {maze.player.score}")
        else:
            print("Left is not a valid move")
    
    def move_right(event):
        new_index = maze.player.index_location
        new_index = (new_index[0]+1, new_index[1])
        if maze.is_cell_reachable(maze.player.index_location, new_index):
            maze.player.index_location = new_index
            maze.player.centre.x += maze.cell_size_x
            maze.player_counter = window.update_player(maze.player_counter, maze.player)
            maze.player.score -= maze.cells[new_index].nearest_dead_end
            maze.cells[new_index].nearest_dead_end = 0
            window.delete_item(maze.dead_end_markers[new_index])
            print(f"Moving Right. Player score now {maze.player.score}")
        else:
            print("Right is not a valid move")


    window.root_widget.bind("<Up>", lambda event: move_up(event))
    window.root_widget.bind("<Down>", lambda event: move_down(event))
    window.root_widget.bind("<Left>", lambda event: move_left(event))
    window.root_widget.bind("<Right>", lambda event: move_right(event))
    window.root_widget.mainloop()