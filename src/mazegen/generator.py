from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from mazegen.config.config_errors import Config
from mazegen.grid.grid import Grid
if TYPE_CHECKING:
    from mazegen.algorithm.imperfect import MazeImperfect


class MazeGenerator(Grid, ABC):
    def __init__(self: "MazeGenerator", config: Config) -> None:
        super().__init__(config)

    @abstractmethod
    def generate(self: "Grid") -> None:
        pass

    @classmethod
    def generate_maze(cls: "type[MazeGenerator]",
                      config: Config) -> "MazeGenerator | MazeImperfect":

        from mazegen.algorithm.dfs_algo import MazeDFS
        from mazegen.algorithm.imperfect import MazeImperfect

        maze: MazeGenerator
        maze = MazeDFS(config)
        maze.generate()

        if config.perfect == "false":
            imperfect_maze = MazeImperfect(config, maze)
            imperfect_maze.make_imperfect()
            return imperfect_maze

        return maze
