class ColorTheme:
    THEMES: dict[int, "ColorTheme"] = {}

    def __init__(self: "ColorTheme", name: str, walls: int, entry: int,
                 exit: int, path: int, fill_42: int) -> None:
        self.name = name
        self.walls = walls
        self.entry = entry
        self.exit = exit
        self.path = path
        self.fill_42 = fill_42

    @classmethod
    def initialze_themes(cls: "type[ColorTheme]") -> None:
        cls.THEMES = {
            0: cls(
                name="default",
                walls=-1,
                entry=-1,
                exit=-1,
                path=6,
                fill_42=7
            ),
            1: cls(
                name="red",
                walls=88,
                entry=166,
                exit=164,
                path=211,
                fill_42=124
            ),
        }

    @classmethod
    def get_theme(cls: "type[ColorTheme]", theme_id: int) -> "ColorTheme":
        if not cls.THEMES:
            cls.initialze_themes()
        return cls.THEMES[theme_id]

    @classmethod
    def get_theme_count(cls: "type[ColorTheme]") -> int:
        if not cls.THEMES:
            cls.initialze_themes()
        count = 0
        for theme in cls.THEMES:
            count += 1
        return count


ColorTheme.initialze_themes()
