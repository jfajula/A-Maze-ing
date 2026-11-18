from __future__ import annotations
from typing import TYPE_CHECKING

from mazegen.grid.cell import Cell
from mazegen.grid.grid import Grid
if TYPE_CHECKING:
    from mazegen.config.config_errors import Config
    from mazegen.generator import MazeGenerator


class MazeImperfect(Grid):
    def __init__(self: "MazeImperfect", config: Config,
                 maze: MazeGenerator) -> None:
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.perfect = config.perfect
        self.grid = maze.grid

    def get_internal_walls(self: "MazeImperfect") -> list[tuple[Cell, int]]:
        total_walls = []

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.is_42:
                    continue

                for dir in [Cell.EAST, Cell.SOUTH]:
                    neighbor = self.get_neighbor(cell, dir)
                    if neighbor is None or neighbor.is_42:
                        continue
                    if cell.has_wall(dir):
                        total_walls.append((cell, dir))
        return total_walls

    def check_2x2(self: "MazeImperfect", cell: "Cell", dir: int) -> bool:
        (x, y) = cell.pos
        tr = self.get_neighbor(cell, Cell.EAST)
        if tr is None or tr.is_42:
            return False
        bl = self.get_neighbor(cell, Cell.SOUTH)
        if bl is None or bl.is_42:
            return False
        br = self.get_neighbor(bl, Cell.EAST)
        if br is None or br.is_42:
            return False
        if dir == Cell.EAST:
            if bl.has_wall(Cell.NORTH) or bl.has_wall(Cell.EAST) \
               or br.has_wall(Cell.NORTH):
                return False
        if dir == Cell.SOUTH:
            if tr.has_wall(Cell.WEST) or tr.has_wall(Cell.SOUTH) \
               or br.has_wall(Cell.WEST):
                return False
        return True

    def check_opening(self: "MazeImperfect", cell: Cell, dir: int) -> bool:
        (x, y) = cell.pos
        if dir == Cell.SOUTH:
            res_right = self.check_2x2(cell, dir)
            cell_left = self.get_neighbor(cell, Cell.WEST)
            if cell_left is None:
                return False
            res_left = self.check_2x2(cell_left, dir)
            return res_right or res_left
        elif dir == Cell.WEST:
            res_down = self.check_2x2(cell, dir)
            cell_top = self.get_neighbor(cell, Cell.NORTH)
            if cell_top is None:
                return False
            res_top = self.check_2x2(cell_top, dir)
            return res_down or res_top
        return True

    def make_imperfect(self: "MazeImperfect", rate: float = 0.1) -> None:
        total_walls = self.get_internal_walls()

        num_to_rmv = int(len(total_walls) * rate)
        num_rmvd = 0
        for cell, dir in total_walls:
            if num_rmvd >= num_to_rmv:
                break

            if not self.check_opening(cell, dir):
                self.rmv_wall_btw(cell, dir)
                num_rmvd += 1
