from __future__ import annotations
from typing import TYPE_CHECKING

from mazegen.grid.cell import Cell
if TYPE_CHECKING:
    from mazegen.grid.grid import Grid


class MazeSolver:
    def __init__(self: "MazeSolver", maze: Grid) -> None:
        self.maze = self.reset_visited(maze)

    def reset_visited(self: "MazeSolver", maze: Grid) -> Grid:
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if cell and cell.is_42 is False:
                    cell.visited = False
        return maze

    def find_open_neighbors(self: "MazeSolver",
                            current: Cell,
                            queue: list[Cell],
                            parents: dict[Cell, tuple[Cell, int] | None]
                            ) -> None:
        for dir in Cell.get_dirs():
            if current.has_wall(dir):
                continue

            neighbor = self.maze.get_neighbor(current, dir)
            if neighbor and neighbor.visited is False:
                neighbor.visited = True
                queue.append(neighbor)
                parents[neighbor] = (current, dir)

    def reconstruct_path(self: "MazeSolver",
                         parents: dict[Cell, tuple[Cell, int] | None],
                         end: Cell) -> list[int]:
        solution = []

        current = end
        while parents[current] is not None:
            parent, dir = parents[current]
            solution.append(dir)
            current = parent

        solution.reverse()
        return solution

    def solve_maze(self: "MazeSolver") -> list[int] | None:
        start = self.maze.get_cell(self.maze.entry[0], self.maze.entry[1])
        end = self.maze.get_cell(self.maze.exit[0], self.maze.exit[1])
        if start is None or end is None:
            return None

        start.visited = True
        queue = [start]
        parents: dict[Cell, tuple[Cell, int] | None] = {start: None}

        while queue:
            current = queue.pop(0)
            if current == end:
                return self.reconstruct_path(parents, end)
            self.find_open_neighbors(current, queue, parents)

        return None
