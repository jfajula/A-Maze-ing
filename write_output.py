from mazegen.config.config_errors import Config
from mazegen.grid.cell import Cell
from mazegen.grid.grid import Grid


class OutputWriter:
    def __init__(self: "OutputWriter", maze: Grid, solution: list[int] | None,
                 config: Config) -> None:
        self.maze = maze
        self.solution = solution
        self.entry = config.entry
        self.exit = config.exit
        self.output = config.output

    def write_output_file(self: "OutputWriter") -> None:
        hex = "0123456789ABCDEF"
        str = ""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                str += hex[self.maze.grid[y][x].walls % 16]
            str += "\n"

        str += "\n"
        (x, y) = self.entry
        str += f"{x},{y}\n"
        (x, y) = self.exit
        str += f"{x},{y}\n"

        if self.solution is not None:
            for dir in self.solution:
                dir_str = Cell.dir_to_str(dir)
                if dir_str is not None:
                    str += dir_str

        str += "\n"
        try:
            with open(self.output, "w") as fd:
                fd.write(str)
        except OSError as e:
            raise OSError("OSError: ", e)
