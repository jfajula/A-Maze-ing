# Mazegen - A maze generation package

A Python package for generating a maze based on a user defined configuration.

## Features
- **Configurable**: User can configure the maze's height and width, entry and exit points.
- **Perfect & Imperfect Mazes**: User can choose to generate a perfect or an imperfect maze.

## Installation

    pip install mazegen-1.0.0-py3-none-any.whl

### Requirements
Python 3.10 or higher

## Example usage

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

## Configurations
- **WIDTH**: Maze width in number of cells
- **HEIGHT**: Maze height
- **ENTRY**: Entry coordinates (x,y)
- **EXIT**: Exit coordinates (x,y)
- **OUTPUT_FILE**: Output filename
- **PERFECT**: Generate perfect maze or not

## Maze and solution path representation
The maze is represented as a 2D int array with the first dimension representing the rows and the second dimension representing the columns.

Each int in the array represents a cell and the value of the int represents which walls of the cell are closed.
A cell is an int from 0 to 15, where the last 4 bits represents the walls.
The walls are each represented by 1 bit.
0 means the wall is open, 1 means the wall is closed.
The north wall is the first bit (LSB), the east wall is the second bit, the south wall is the third bit, the west wall is the 4th bit.
For example, 3 (binary 0011) means the cell is open to the south and west.

The solution path is represented as a list of int with each int representing a direction to go starting from the entry point to the exit point.
1 represents going north, 2 represents going east, 4 represents going south, 8 represents going west.


## Core classes
- `MazeGenerator`: Main interface for maze generation.
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
