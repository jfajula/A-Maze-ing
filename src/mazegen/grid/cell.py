class Cell:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self: "Cell", pos: tuple[int, int], visited: bool = False,
                 walls: int = 15, is_42: bool = False) -> None:
        self.pos = pos
        self.visited = visited
        self.walls = walls
        self.is_42 = is_42

    @classmethod
    def get_dirs(cls: "type[Cell]") -> list[int]:
        return [cls.NORTH, cls.EAST, cls.SOUTH, cls.WEST]

    @classmethod
    def dir_to_str(cls: "type[Cell]", dir: int) -> str | None:
        """Converts a diretion to its corresponding name."""
        if dir == cls.NORTH:
            return "N"
        if dir == cls.EAST:
            return "E"
        if dir == cls.SOUTH:
            return "S"
        if dir == cls.WEST:
            return "W"

        return None

    def has_wall(self: "Cell", dir: int) -> bool:
        if self.walls & dir:
            return True
        return False

    def rmv_wall(self: "Cell", dir: int) -> None:
        if not self.is_42:
            self.walls = self.walls & ~dir
