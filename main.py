
from mazetools import generate_and_solve_maze, generate_maze, set_up_playing_maze, make_interactive
from window import Window

def main():

    window = Window(800, 600)
    maze = set_up_playing_maze(window, 'l')

    make_interactive(maze, window)
    
    window.wait_for_close()
    print("hello world")

if __name__ == "__main__":
    main()
