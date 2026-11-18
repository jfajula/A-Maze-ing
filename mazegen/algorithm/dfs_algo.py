import random

from mazegen.config.config_errors import Config, ConfigError
from mazegen.generator import MazeGenerator


class MazeDFS(MazeGenerator):
    def __init__(self: "MazeDFS", config: Config) -> None:
        super().__init__(config)

    def generate(self: "MazeDFS") -> None:

        start = self.get_cell(self.entry[0], self.entry[1])
        if start is None:
            raise ConfigError("Start cell cannot be None")
        if start.visited:
            raise ConfigError("Start cell already visited")
        if start.is_42:
            raise ConfigError("Start cell cannot be inside 42 pattern")

        start.visited = True
        stack = [start]

        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                neighbor, direction = random.choice(neighbors)
                self.rmv_wall_btw(current, direction)
                neighbor.visited = True
                stack.append(neighbor)
            else:
                stack.pop()