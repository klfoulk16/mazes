"""Creates a random binary maze and prints it out"""
import random
from PIL import Image

# width and height must be odd numbers
def initialize_maze(width, height):
    # create empty set of set size
    maze = [[0 for i in range(width)] for j in range(height)]

    # add borders
    add_borders(maze, width, height)

    build_walls(maze, 0, height, 0, width)

    # add start and end points
    maze[1][1] = "Start"
    maze[width-2][height-2] = "End"

    return maze

def add_borders(maze, width, height):
    # add top and bottom walls
    for i in range(width):
        maze[0][i] = 1
        maze[height-1][i] = 1

    for i in range(height):
        maze[i][0] = 1
        maze[i][width-1] = 1

    return maze


def build_walls(maze, top, bottom, left, right):
    direction = None
    # create verticle or horizontal wall?
    if (right - left) < (bottom - top):
        direction = "horizontal"
    elif (right - left) > (bottom - top):
        direction = "verticle"
    else:
        direction = random.choice(["horizontal", "verticle"])

    # use recursive function to divide maze into two small rectangles until finished...

    # walls only build on evens (with top border being 0). paths only built on odds.
    if direction == "horizontal":
        wall = random.randrange(top + 2, bottom - 1, 2)
        # go from left to right building the wall.
        for x in range(left, right):
            maze[wall][x] = 1
        # get odd number to be the path through the wall
        path = random.randrange(left + 1, right, 2)
        maze[wall][path] = 0
        # redo for top half if there's enough room to make a new wall
        if wall - top > 3:
            build_walls(maze, top, wall, left, right)
        # redo for the bottom half if there's enough room to make a new wall
        if bottom - wall > 3:
            build_walls(maze, wall, bottom, left, right)

    if direction == "verticle":
        wall = random.randrange(left + 2, right - 1, 2)
        for y in range(top, bottom):
            maze[y][wall] = 1
        path = random.randrange(top + 1, bottom - 1, 2)
        maze[path][wall] = 0
        # continue left half if there's enough room
        if wall - left > 3:
            build_walls(maze, top, bottom, left, wall)
        # continue on the right half if there's enough room
        if right - wall > 3:
            build_walls(maze, top, bottom, wall, right)
    return maze

def write_img(maze, width, height):
    """Creates a small img of the new maze"""
    img = Image.new( 'RGB', (width, height))
    pixels = img.load()
    for i in range(height):
        for j in range(width):
            if maze[i][j] == "Start":
                pixels[i,j] = (0, 255, 0)
            elif maze[i][j] == "End":
                pixels[i,j] = (255, 0, 0)
            elif maze[i][j] == 1:
                pixels[i,j] = (0, 0, 0)
            else:
                pixels[i,j] = (255, 255, 255)
    img.show()

def main():

    width = 11
    height = 11

    maze = initialize_maze(width, height)

    write_img(maze, width, height)

main()
