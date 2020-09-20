import random
from PIL import Image

"""Contains the objects necessary to create and solve various mazes.
Order from top to bottom: Cell, StackFrontier, Queuefrontier, Maze"""

class Cell():
    """Structure to keep track of various cells in the maze and which cell we used to get there"""
    def __init__(self, location, parent_cell, end_cell):
        self.location = location
        self.parent = parent_cell
        # set start cell "steps" to 0. If not start cell, set it to 1 more than the parent cell's.
        # This measures how many steps along a direct path we took to get to this cell.
        # This also sets end cells steps to 0
        if self.parent != None:
            self.steps = parent_cell.steps + 1
        else:
            self.steps = 0

        # if the cell we're initializing isn't the end cell, calculate estimated_distance
        if end_cell != None:
            self.estimated_distance = self.calc_distance(location, self.steps, end_cell)
        else:
            self.estimated_distance = 0

    def calc_distance(self, location, parent, end_cell):
        # calculate absolute distance away from end point
        horz_distance = end_cell.location[0] - self.location[0]
        vert_distance = end_cell.location[1] - self.location[1]
        absolute_distance = vert_distance + horz_distance

        # add steps to absolute_distance to get estimate of how 'good' a path this cell is on
        total_estimated_distance = absolute_distance + self.steps
        #if self.parent != None:
            #print(f"New Cell location: {self.location[0]},{self.location[1]} steps: {self.steps}, abs: {absolute_distance}, total: {total_estimated_distance}")
        return total_estimated_distance



class StackFrontier():
    """Last in, first out data structure. Use this for Depth First Search."""
    def __init__(self):
        self.frontier = []

    def add(self, cell):
        self.frontier.append(cell)

    def return_parent(self, parent):
        for cell in self.frontier:
            if cell.location == parent:
                return cell

    def empty(self):
        return len(self.frontier) == 0

    def remove(self, explored_cells):
        if self.empty():
            raise Exception("empty frontier")
        else:
            cell = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return cell


class QueueFrontier(StackFrontier):
    """First in, first out data structure. Use this for Breadth First Search."""
    def remove(self, explored_cells):
        if self.empty():
            raise Exception("empty frontier")
        else:
            cell = self.frontier[0]
            self.frontier = self.frontier[1:]
            return cell


class SmartFrontier(StackFrontier):
    """Returns cell with the least estimated_distance, if two have the same estimated_distance,
    it returns the first one it finds. This way it explores the path that shows the most promise,
    given the absolute distance of the cell to the end point and the total # of steps it took to get there."""
    def remove(self, explored_cells):
        if self.empty():
            raise Exception("empty frontier")
        else:
            # distance = number larger than cell.estimated_distance could be
            distance = 1000
            closest_cell = None
            for cell in self.frontier:
                if cell.estimated_distance < distance:
                    distance = cell.estimated_distance
                    closest_cell = cell
                    #print(f"Closest cell: {closest_cell.location}")
                # if there's two cells of equal distance away...
                elif cell.estimated_distance == distance:
                    # if their parent is the start cell, choose randomly
                    if cell.parent.parent == None:
                        closest_cell = random.choice([closest_cell, cell])
                    # else follow current path
                    if cell.parent in explored_cells:
                        closest_cell = cell
            self.frontier.remove(closest_cell)
            #print(f"Chosen cell: {closest_cell.location}, Distance: {closest_cell.estimated_distance}")
            return closest_cell
    def print(self):
        for cell in self.frontier:
            print(cell.estimated_distance)


class Maze():
    """This is the maze you're working with. You can create, solve and print it."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Create set of width*height size filled with 0's (path cells)
        self.board = [[0 for i in range(width)] for j in range(height)]
        # Add all of the walls by changing various 0's to 1's.
        self.add_borders()
        self.build_walls(0, self.height, 0, self.width)
        # Label start and end points. Change maze values to ensure they aren't walls.
        self.end = Cell((self.width-2,self.height-2), None, None)
        self.start = Cell((1,1), None, self.end)
        self.board[1][1] = "Start"
        self.board[self.width-2][self.height-2] = "End"

    def add_borders(self):
        # Add walls along the edge of the maze.
        for i in range(self.width):
            self.board[0][i] = 1
            self.board[self.height-1][i] = 1
        for i in range(self.height):
            self.board[i][0] = 1
            self.board[i][self.width-1] = 1

    def build_walls(self, top, bottom, left, right):
        """Uses recursive division to add maze walls. Based off idea from this webpage:
         http://weblog.jamisbuck.org/2011/1/12/maze-generation-recursive-division-algorithm"""
        # Decide whether to add vertical or horizontal wall.
        # Add horizontal if maze section's height is greater than it's width.
        # Add verticle section otherwise. Random if height and width are even.
        direction = None
        if (right - left) < (bottom - top):
            direction = "horizontal"
        elif (right - left) > (bottom - top):
            direction = "vertical"
        else:
            direction = random.choice(["horizontal", "vertical"])
        # Recursively divide maze into two smaller rectangles. In each rectangle,
        # add one wall that spans the entire length of the rectangle at a random
        # even index (top = 0). Do this by changing the 0's to 1's. Add one
        # opening through each of the walls at an even index by changing the 1 back to 0.
        # Repeat for the section above/below or left/right of the wall (depending
        # on whether the wall was verticle or horizontal)until the sections are
        # too small to add walls to.
        if direction == "horizontal":
            wall = random.randrange(top + 2, bottom - 1, 2)
            # go from left to right building the wall.
            for x in range(left, right):
                self.board[wall][x] = 1
            # get odd number to be the path through the wall
            path = random.randrange(left + 1, right, 2)
            self.board[wall][path] = 0
            # redo for top half if there's enough room to make a new wall
            if wall - top > 3:
                self.build_walls(top, wall, left, right)
            # redo for the bottom half if there's enough room to make a new wall
            if bottom - wall > 3:
                self.build_walls(wall, bottom, left, right)
        if direction == "vertical":
            wall = random.randrange(left + 2, right - 1, 2)
            for y in range(top, bottom):
                self.board[y][wall] = 1
            path = random.randrange(top + 1, bottom - 1, 2)
            self.board[path][wall] = 0
            # redo for left half if there's enough room
            if wall - left > 3:
                self.build_walls(top, bottom, left, wall)
            # redo for right half if there's enough room
            if right - wall > 3:
                self.build_walls(top, bottom, wall, right)

    def solve(self, frontier):
        # Create an empty set to populate with the cells we explore.
        self.explored_cells = set()
        # Explore cells until we find the end point
        self.explore_paths(self.start, frontier)
        # identify the direct path. Marks cells as "P" and creates a set of the final path cells.
        self.trace_final_path()

    def explore_paths(self, current_cell, frontier):
        """Recursively explores neighbors of each cell along the various maze paths until it finds the end point. It marks all cells that it explores as "E" in the board and adds them to the set of explored cells."""
        # shuffle the list of possible neighbor locations so that we explore the cells in random order
        neighbors = (-1,0), (0,-1), (0,1), (1,0)
        neighbors = list(neighbors)
        random.shuffle(neighbors)
        # iterate over neighbors to the current cell to see if they are either path cells or the end point
        for (i,j) in neighbors:
            for x,y in [(current_cell.location[0]+i,current_cell.location[1]+j)]:
                if x in range(0, self.width) and y in range(0, self.height):
                    # 2) if one of the neighbors is the end, update the parent of the end cell
                    if self.board[x][y] == "End":
                        self.end.parent = current_cell
                        return True
                    # If cell is a path cell, add it to the frontier to be (potentially) explored
                    elif self.board[x][y] == 0:
                            new_cell = Cell((x,y), current_cell, self.end)
                            frontier.add(new_cell)
        # 4) pop a cell off of the frontier (which cell gets removed depends on the type of frontier)
        # choosing a cell:
        current_cell = frontier.remove(self.explored_cells)
        #print(f"Chosen cell: {current_cell.location[0]}, {current_cell.location[1]}")
        # 5) add cell to explored_cells and mark it as "E" for visualization
        self.explored_cells.add(current_cell)
        self.board[current_cell.location[0]][current_cell.location[1]] = "E"
        # 6) repeat steps 1-5 until you find the end point
        self.explore_paths(current_cell, frontier)

    def trace_final_path(self):
        """Works backwards to identify the path taken to get to the end cell.
        Marks them as P for easy visualization."""
        # create set of cells for path, starting with end cell
        self.final_path = {self.end}
        # loop over explored cells until we find the cell who's parent was the start point (1,1)
        current_cell = self.end
        while current_cell.parent.location != self.start.location:
            # use cell.parent to find the cell we used to get to the current cell
            for cell in self.explored_cells:
                if current_cell.parent.location == cell.location:
                    # add to path set and switch cell value from "E" to "P"
                    self.final_path.add(cell)
                    self.board[cell.location[0]][cell.location[1]] = "P"
                    current_cell = cell

    def print_maze_img(self, type):
        """
        Creates a small img of the maze.
        Usage: type is version of the maze you want to print...
        Finished_path -- shows the path the algorithm found.
        Finished_explored -- shows all of the cells explored.
        Unfinished -- the unfinished maze.
        """
        img = Image.new( 'RGB', (self.width, self.height))
        pixels = img.load()
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 1:
                    pixels[i,j] = (0, 0, 0)
                if self.board[i][j] == 0:
                    pixels[i,j] = (255, 255, 255)
                if self.board[i][j] == "Start":
                    pixels[i,j] = (0, 255, 0)
                elif self.board[i][j] == "End":
                    pixels[i,j] = (255, 0, 0)
                elif self.board[i][j] == "E":
                    if type in ["unfinished", "finished_path"]:
                        pixels[i,j] = (255, 255, 255)
                    else:
                        pixels[i,j] = (0, 0, 255)
                elif self.board[i][j] == "P":
                    if type in ["finished_explored", "finished_path"]:
                        pixels[i,j] = (0, 255, 0)
                    else:
                        pixels[i,j] = (255, 255, 255)
        img.show()

    def print_maze_terminal(self):
        """Prints out the binary maze in the terminal."""
        for row in range(self.height):
            print(self.board[row])

    def percent_explored(self):
        """Return percent of maze explored (not including walls)."""
        total = 0
        total_explored = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] in ["E", "P"]:
                    total_explored += 1
                    total += 1
                elif self.board[i][j] == 0:
                    total += 1
        percent = int((total_explored/total)*100)
        return percent
