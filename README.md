# mazes
Tested the efficiency (% of cells explored) of various search algorithms for solving mazes. This project also creates and solves binary mazes. 

What I did:
1) Designed a recursive division function to create the mazes. 
2) Used Pillow to print out a small png file img (zoom in to see the image better) so that I can visualize the maze better. 
3) Used Breadth First Search, Depth First Search, and a "Smart" algorithm (inspired by the one explained by Brian Yu in Harvard's AI with python course) to solve the mazes.
4) Tested the algorithms against each other on a series of 500 mazes to see which is the most efficient...efficiency refering to percentage of the maze explored before the end point was found.

To use:
Run main.py as is to see an example of the Smart Algorthm solving a maze (a small image will be printed out showing cells explored and the final path) and to compare the efficiency of the different algorithms (the average % of the maze that each algorithm explored will be printed to your terminal window).

To see how Depth First Search solves a maze, pass StackFrontier() to the visualization() function. Ex:
visualization(21, StackFrontier())

To see how Breadth First Search solves a maze, pass QueueFrontier() to the visualization() function. Ex:
visualization(21, QueueFrontier())
