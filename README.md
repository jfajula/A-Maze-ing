*This project has been created as part of the 42 curriculum by jafajula and jorvilch.*

# A-Maze-ing
## Description
This project implements a maze generator in Python that takes a configuration file, generates a maze based on the given configuration, writes the maze, entry and exit points and the shortest solution to an outputfile, and also visualize the results.

All generated mazes contain a "42" pattern at the center consisting of fully closed cells, unless the maze is too small for the pattern (smaller than 7 x 5). In this case, a maze without the "42" pattern will be generated.

### Maze generation algorithm
The following algorithm is implemented to generate the maze:

#### Depth-First Search (DFS) algorithm
DFS works by

- step 1: Start with a grid where every cell is surrounded by walls.
- step 2: Pick a starting cell.
- step 3: Choose a random unvisited neighbor.
- step 4: Remove the wall between the current cell and that neighbor.
- step 5: Move to the neighbor and repeat.
- step 6: If a cell has no unvisited neighbors, backtrack to the previous cell.

Continue until all cells are visited.
#### Creating imperfect maze
DFS create perfect mazes.
To generate imperfect mazes, we randonly remove some walls in the perfect mazes.
In this way, the paths are connected in more than one ways and thus creates multiple solutions.

The default setting removes 50% of the walls. This percentage can be changed by passing a float between 0 and 1 to the `make_imperfect()` function in `maze_generator.py`.

The wall removal follows the constraint that the open areas cannot be wider than 2 cells.

### Maze solving algorithm: Breadth-First Search (BFS)
BFS explores the maze level by level (n steps away from the entry cell). The shortest path is found as soon as the exit cell is reached.

- Step 1: Start from he entry cell, mark it as visited, add it to the queue (to be processed), set its parent (previous cell in the path) to be None.
- Step 2: Add unvisited neighbors that are open to the current cell to the queue and set their parents to the current cell.
- Step 3: Remove the current cell from the queue and set the next one as the current cell.
- Step 4: Repeat Step 2 - 3 until the exit cell is found.
- Step 5: Reconstruction the solution from the exit cell using the stored parent information.

BFS is chosen because it is suitable for unweighted graphs, which is the case for our maze.
BFS only need to traverse the graph once to find the shortest path, making it time-efficient.


## Instructions

Install dependencies:

    make install

Run the program:

    make run
       or
    python3 a_maze_ing.py config.txt

Run the program in debug mode:

    make debug

Remove temporary files and caches:

    make clean

Code linting using `flake8` and `mypy`

    make lint


### Configuration file format
#### Mandatory keys:
| Key | Description | Example |
|----|-------------|---------|
| WIDTH | Maze width in number of cells | WIDTH=10 |
| HEIGHT | Maze height | HEIGHT=10 |
| ENTRY | Entry coordinates (x,y) | ENTRY=0,0 |
| EXIT | Exit coordinates (x,y) | EXIT=9,9 |
| OUTPUT_FILE | Output filename | OUTPUT_FILE=maze.txt |
| PERFECT | Generate perfect maze or not | PERFERCT=True |

### Reusable module
The maze generation and solution part of the project is packaged as the `mazegen` reusable module.

#### Installation

    pip install mazegen-1.0.0-py3-none-any.whl

##### Requirements
Python 3.10 or higher

#### Example usage

    from mazegen.config import Config
    from mazegen.generator import MazeGenerator
    from mazegen.solve.solver import MazeSolver

    # Configuration
    config_dict = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": "True",
    }
    config = Config(config_dict)

    # Generate maze
    maze = MazeGenerator.generate_maze(config)

    # Find the shortest solution
    solution = MazeSolver(maze).solve_maze()

#### Configurations
- **WIDTH**: Maze width in number of cells
- **HEIGHT**: Maze height
- **ENTRY**: Entry coordinates (x,y)
- **EXIT**: Exit coordinates (x,y)
- **OUTPUT_FILE**: Output filename
- **PERFECT**: Generate perfect maze or not

#### Maze and solution path representation
The maze is represented as a 2D int array with the first dimension representing the rows and the second dimension representing the columns.

Each int in the array represents a cell and the value of the int represents which walls of the cell are closed.
A cell is an int from 0 to 15, where the last 4 bits represents the walls.
The walls are each represented by 1 bit.
0 means the wall is open, 1 means the wall is closed.
The north wall is the first bit (LSB), the east wall is the second bit, the south wall is the third bit, the west wall is the 4th bit.
For example, 3 (binary 0011) means the cell is open to the south and west.

The solution path is represented as a list of int with each int representing a direction to go starting from the entry point to the exit point.
1 represents going north, 2 represents going east, 4 represents going south, 8 represents going west.


#### Core classes
- `##MazeGenerator`: Main interface for maze generation.
- `Grid`: Representation of a maze with the following attributes:
    - width (int)
    - height (int)
    - entry (tuple[int, int])
    - exit (tuple[int, int])
    - grid (list[list[Cell]]): The grid in the form of a 2D array of `Cell` objects.
- `Cell`: Representation of a cell in the maze withe the following attributes:
    - pos (tuple[int, int]): Position of the cell in the maze.
    - visited (bool): Whether the cell has been visited or not.
    - walls (int): An interger from 0 to 15 that signifies which walls of the cell are open.
    - is_42 (bool): Whether the cell is part of the 42 pattern.
- `MazeSolver`: Find the shortest solution path from entry to exit using the Breadth-First Search (BFS) algorithm (`solve_maze()`). The solution is represented as a list of int.
- `Config`: Set the configuration of the maze from a dictionary.

### Visualization
This project uses the `curses` module to render the maze on the terminal with the following user interactions:

- Use the arrow keys ← ↑ → ↓ to scroll the curses window.
- Press i to enter input mode.
- Input 1 to regenerate a new maze.
- Input 2 to show or hide the shortest solution path.
- Input 3 to rotate maze colors.
- Input 4 to quit

### Output file format
The output file consists of the following parts:
- the maze printed as a grid, where each cell is represented as a hexadecimal digit,
- the entry coordinates x,y,
- the exit coordinates x,y,
- the shortest solution path as a sequence of directions (N/E/S/W) from the entry to the exit.

## Project management

### Task divisions
All the code was done by jafajula

### Initial planning and evolution
We initialy planned to use the MLX library. But after some search, we decided to use the Python build-in `curses` library for a terminal rendering.

### Reflections
The whole project ended being done by the same person and that is an errors caused by being too close to the blackhole date

We could have planned better and have clearer task divisions since the beginning with some more time.

## Resources
- https://docs.python.org/3/
- https://en.wikipedia.org/wiki/Breadth-first_search
- https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/
- https://en.wikipedia.org/wiki/Depth-first_search
- https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/


### Tools used
- **venv**: Create virtual environment
- **git**: Version control
- **pip**: Package manager
- **build**: Package builder
- **flake8**: Code linting and style checking
- **mypy**: Static type checker for Python

AI wasn't used in any step of the project
