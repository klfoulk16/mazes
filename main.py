from util import Cell, StackFrontier, QueueFrontier, SmartFrontier, Maze
import copy

"""Goals of this project: Become comfortable working with recursion, objects, and search algorithms.
"""

def main():
    # demostrates the project creating and solving a maze using my "Smart" algorithm.
    # to use BFS or DPS pass in StackFrontier() for DFS or QueueFrontier for BFS
    # the number passed into visualization must be odd and less than 60
    visualization(21, SmartFrontier())
    # determines the % cells explored for each algorithm to show their efficiency.
    compare_algorithms()


# you must pass in a odd number less than 60 for size
def visualization(size, frontier):
    """Currently creates a size*size binary maze. Solves it using your chosen algorithm. Prints out a small image of the unfinished maze and one of the solved maze for visualization."""
    frontier = frontier
    maze = Maze(size,size)
    maze.solve(frontier)
    maze.print_maze_img("finished_explored")
    maze.print_maze_img("unfinished")


def compare_algorithms():
    """Runs the three different search algorithms over a series of 500 mazes and then calculates the average % of maze cells explored for each algorithm."""
    breadth_av = 0
    depth_av = 0
    smart_av = 0
    test_count = 500

    for i in range(test_count):
        # create mazes and frontiers
        depth_frontier = StackFrontier()
        breadth_frontier = QueueFrontier()
        smart_frontier = SmartFrontier()

        # increase the below number from 21 and you risk getting a maximum recursion depth error
        depth_maze = Maze(21,21)
        breadth_maze = copy.deepcopy(depth_maze)
        smart_maze = copy.deepcopy(depth_maze)

        # solve mazes
        depth_maze.solve(depth_frontier)
        breadth_maze.solve(breadth_frontier)
        smart_maze.solve(smart_frontier)

        # get percent
        depth_av += depth_maze.percent_explored()
        breadth_av += breadth_maze.percent_explored()
        smart_av += smart_maze.percent_explored()

    # divide av by range
    breadth_av = int(breadth_av/test_count)
    depth_av = int(depth_av/test_count)
    smart_av = int(smart_av/test_count)

    print(f"BFS Average: {breadth_av}%")
    print(f"DFS Average: {depth_av}%")
    print(f"Smart Average: {smart_av}%")


if __name__ == "__main__":
    main()
