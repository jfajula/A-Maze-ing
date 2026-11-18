from mazegen.config.config_errors import Config, ConfigError
from mazegen.grid.cell import Cell

class Grid:
    def __init__(self: "Grid", config: Config) -> None:
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.perfect = config.perfect
        self.grid = self.make_grid()
        if self.width >= 7 and self.height >= 5:
            self.make_42()

    def make_grid(self: "Grid") -> list[list[Cell]]:
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell((x, y))
                row.append(cell)
            grid.append(row)
        return grid

    def make_42(self: "Grid") -> None:
        pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        center_x = self.width // 2
        center_y = self.height // 2

        start_x = center_x - pattern_width // 2
        start_y = center_y - pattern_height // 2
        for py in range(pattern_height):
            for px in range(pattern_width):
                grid_x = start_x + px
                grid_y = start_y + py

                if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                    if pattern[py][px] == 1:
                        cell = self.grid[grid_y][grid_x]
                        cell.is_42 = True
                        cell.walls = 15
                        cell.visited = True

        entry_cell = self.get_cell(self.entry[0], self.entry[1])
        exit_cell = self.get_cell(self.exit[0], self.exit[1])
        if entry_cell is None or exit_cell is None:
            raise ConfigError("ConfigError: "
                              "Entry or exit cell is None.")
        if entry_cell.is_42 is True:
            raise ConfigError("ConfigError: "
                              "Entry point is inside 42 pattern.")
        if exit_cell.is_42 is True:
            raise ConfigError("ConfigError: "
                              "Exit point is inside 42 pattern.")

    def get_cell(self: "Grid", x: int, y: int) -> Cell | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_neighbor(self: "Grid", cell: Cell, direction: int) -> Cell | None:
        x, y = cell.pos
        if direction == Cell.NORTH:
            neighbor = self.get_cell(x, y - 1)
        elif direction == Cell.EAST:
            neighbor = self.get_cell(x + 1, y)
        elif direction == Cell.SOUTH:
            neighbor = self.get_cell(x, y + 1)
        elif direction == Cell.WEST:
            neighbor = self.get_cell(x - 1, y)
        else:
            return None
        return neighbor

    def get_unvisited_neighbors(self: "Grid",
                                cell: Cell) -> list[tuple[Cell, int]]:
        neighbors = []

        for direction in Cell.get_dirs():
            neighbor = self.get_neighbor(cell, direction)
            if neighbor and not neighbor.visited and not neighbor.is_42:
                neighbors.append((neighbor, direction))
        return neighbors

    def get_visited_neighbors(self: "Grid",
                              cell: Cell) -> list[tuple[Cell, int]]:
        neighbors = []

        for direction in Cell.get_dirs():
            neighbor = self.get_neighbor(cell, direction)
            if neighbor and neighbor.visited and not neighbor.is_42:
                neighbors.append((neighbor, direction))
        return neighbors

    @staticmethod
    def get_opposite_direction(direction: int) -> int:
        opposites = {
            Cell.NORTH: Cell.SOUTH,
            Cell.SOUTH: Cell.NORTH,
            Cell.EAST: Cell.WEST,
            Cell.WEST: Cell.EAST
        }
        return opposites[direction]

    def rmv_wall_btwn(self: "Grid", cell: Cell, direction: int) -> None:
        if cell.is_42:
            return

        neighbor = self.get_neighbor(cell, direction)
        if neighbor is None or neighbor.is_42:
            return

        cell.rmv_wall(direction)
        opp_dir = self.get_opposite_direction(direction)
        neighbor.rmv_wall(opp_dir)
