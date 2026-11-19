import curses

from mazegen.config.config_errors import Config
from mazegen.grid.grid import Grid
from mazegen.generator import MazeGenerator
from mazegen.solve.solver import MazeSolver
from write_output import OutputWriter
from mazedisp.maze import MazePainter
from mazedisp.colors import ColorTheme


class MazeDisplay:
    def __init__(self: "MazeDisplay", stdscr: curses.window,
                 config: Config) -> None:
        self.stdscr = stdscr
        self.config = config
        self.screen_height = 0
        self.screen_width = 0
        self.scroll_offset_y = 0
        self.scroll_offset_x = 0
        self.total_height = 0
        self.total_width = 0
        self.menu_height = 11
        self.prompt_row = 0
        self.prompt_col = len("Choice? (1-4): ")
        self.current_theme = 0
        self.pad: curses.window | None = None
        self.painter: MazePainter | None = None
        self.maze: Grid | None = None
        self.solution: list[int] | None = None
        self.solution_visible = False

    def generate_maze(self: "MazeDisplay") -> None:
        self.maze = MazeGenerator.generate_maze(self.config)

        self.solution = MazeSolver(self.maze).solve_maze()

        output = OutputWriter(self.maze, self.solution, self.config)
        output.write_output_file()

    def redraw(self: "MazeDisplay") -> None:
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()

        self.stdscr.refresh()

        if self.pad is None:
            return

        try:
            self.pad.refresh(self.scroll_offset_y, self.scroll_offset_x, 0, 0,
                             self.screen_height - 1, self.screen_width - 1)
        except curses.error:
            pass

    def display_maze(self: "MazeDisplay") -> None:
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()

        self.generate_maze()

        if self.maze is None:
            return

        self.scroll_offset_y = 0
        self.scroll_offset_x = 0

        maze_height = self.maze.height * 2 + 1
        self.total_height = maze_height + self.menu_height
        self.total_width = self.maze.width * 4 + 1

        pad_height = max(self.total_height, self.screen_height)
        pad_width = max(self.total_width, self.screen_width)
        self.pad = curses.newpad(pad_height, pad_width)

        theme = ColorTheme.get_theme(self.current_theme)
        self.painter = MazePainter(self.pad, self.maze, self.solution, theme)
        self.painter.set_pad_refresh_params(self.scroll_offset_y,
                                            self.scroll_offset_x,
                                            self.screen_height,
                                            self.screen_width)

        curses.curs_set(0)

        self.show_choices()
        self.painter.print_walls()
        self.painter.fill_42()
        self.painter.draw_entry_exit("E", 2)
        self.painter.draw_entry_exit("X", 3)

        self.prompt_row = self.maze.height * 2 + 1 + 2 + 7

        self.redraw()

    def show_solution(self: "MazeDisplay") -> None:
        if self.painter:
            self.painter.draw_path()
            self.redraw()

    def hide_solution(self: "MazeDisplay") -> None:
        if self.painter:
            self.painter.clear_path()
            self.redraw()

    def rotate_colors(self: "MazeDisplay") -> None:
        if self.pad is None or self.maze is None:
            return

        self.pad.clear()

        self.current_theme = (self.current_theme + 1) \
            % ColorTheme.get_theme_count()

        theme = ColorTheme.get_theme(self.current_theme)
        self.painter = MazePainter(self.pad, self.maze, self.solution, theme)
        self.painter.set_pad_refresh_params(self.scroll_offset_y,
                                            self.scroll_offset_x,
                                            self.screen_height,
                                            self.screen_width)
        self.show_choices()
        self.painter.print_walls()
        self.painter.fill_42()
        self.painter.draw_entry_exit("E", 2)
        self.painter.draw_entry_exit("X", 3)
        if self.solution_visible:
            self.painter.draw_path()
        self.redraw()

    def show_choices(self: "MazeDisplay") -> None:
        if self.maze is None or self.pad is None:
            return

        start_row = self.maze.height * 2 + 1 + 2

        try:
            self.pad.move(start_row, 0)
            self.pad.addstr(start_row, 0,
                            "=== A-Maze-ing ===", curses.color_pair(6))
            self.pad.addstr(start_row + 1, 0,
                            "Use ← ↑ → ↓ to scroll.", curses.color_pair(6))
            self.pad.addstr(start_row + 2, 0,
                            "Press i to enter input mode.",
                            curses.color_pair(6))
            self.pad.addstr(start_row + 3, 0,
                            "1. Re-generate a new maze", curses.color_pair(6))
            self.pad.addstr(start_row + 4, 0,
                            "2. Show/Hide path from entry to exit",
                            curses.color_pair(6))
            self.pad.addstr(start_row + 5, 0,
                            "3. Rotate maze colors", curses.color_pair(6))
            self.pad.addstr(start_row + 6, 0,
                            "4. Quit", curses.color_pair(6))
            self.pad.addstr(start_row + 7, 0,
                            "Choice? (1-4): ", curses.color_pair(6))
        except curses.error:
            pass

    def display_message(self: "MazeDisplay", message: str) -> None:
        if self.maze is None or self.pad is None:
            return

        start_row = self.maze.height * 2 + 1 + 2 + 8

        try:
            self.pad.move(start_row, 0)
            self.pad.clrtoeol()
            self.pad.addstr(start_row, 0, message, curses.color_pair(6))
        except curses.error:
            pass

    def handle_resize(self: "MazeDisplay") -> None:
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()
        max_scroll_y = max(0, self.total_height - self.screen_height)
        max_scroll_x = max(0, self.total_width - self.screen_width)
        self.scroll_offset_y = min(self.scroll_offset_y, max_scroll_y)
        self.scroll_offset_x = min(self.scroll_offset_x, max_scroll_x)
        self.redraw()

    def scroll_up(self: "MazeDisplay") -> None:
        self.scroll_offset_y = max(0, self.scroll_offset_y - 1)
        self.redraw()

    def scroll_down(self: "MazeDisplay") -> None:
        max_scroll_y = max(0, self.total_height - self.screen_height)
        self.scroll_offset_y = min(max_scroll_y, self.scroll_offset_y + 1)
        self.redraw()

    def scroll_left(self: "MazeDisplay") -> None:
        self.scroll_offset_x = max(0, self.scroll_offset_x - 1)
        self.redraw()

    def scroll_right(self: "MazeDisplay") -> None:
        max_scroll_x = max(0, self.total_width - self.screen_width)
        self.scroll_offset_x = min(max_scroll_x, self.scroll_offset_x + 1)
        self.redraw()

    def scroll_to_prompt(self: "MazeDisplay") -> None:
        if self.prompt_row - self.scroll_offset_y >= self.screen_height - 2 \
                or self.prompt_col <= self.scroll_offset_x:
            calc_y = self.prompt_row - self.screen_height + 2
            self.scroll_offset_y = max(0, calc_y)
            self.scroll_offset_x = 0
            self.redraw()

    def get_user_input(self: "MazeDisplay") -> str:
        if self.pad is None:
            return ""

        prompt_screen_y = self.prompt_row - self.scroll_offset_y
        prompt_screen_x = self.prompt_col - self.scroll_offset_x

        curses.curs_set(1)

        try:
            self.stdscr.move(prompt_screen_y, prompt_screen_x)
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
        except curses.error:
            pass

        res = ""
        cursor_pos = 0

        while True:
            try:
                self.stdscr.move(prompt_screen_y, prompt_screen_x)
                self.stdscr.clrtoeol()
                self.stdscr.addstr(prompt_screen_y, prompt_screen_x, res)
                self.stdscr.move(prompt_screen_y, prompt_screen_x + cursor_pos)
                self.stdscr.refresh()
            except curses.error:
                pass

            key = self.stdscr.getch()

            if key in [curses.KEY_ENTER, 10, 13]:
                break
            elif key in [curses.KEY_BACKSPACE, 127, 8]:
                if cursor_pos > 0:
                    res = res[:cursor_pos-1] + res[cursor_pos:]
                    cursor_pos -= 1
            elif key == curses.KEY_DC:
                if cursor_pos < len(res):
                    res = res[:cursor_pos] + res[cursor_pos+1:]
            elif key == curses.KEY_LEFT:
                if cursor_pos > 0:
                    cursor_pos -= 1
            elif key == curses.KEY_RIGHT:
                if cursor_pos < len(res):
                    cursor_pos += 1
            elif 32 <= key <= 126:
                char = chr(key)
                res = res[:cursor_pos] + char + res[cursor_pos:]
                cursor_pos += 1
                if len(res) > 10:
                    res = res[:10]
                    cursor_pos = min(cursor_pos, 10)

        curses.curs_set(0)

        try:
            self.pad.move(self.prompt_row, self.prompt_col)
            self.pad.clrtoeol()
            self.pad.refresh(self.scroll_offset_y, self.scroll_offset_x,
                             0, 0,
                             self.screen_height - 1, self.screen_width - 1)
        except curses.error:
            pass

        try:
            self.stdscr.move(prompt_screen_y, prompt_screen_x)
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
        except curses.error:
            pass

        return res.strip()

    def handle_user_input(self: "MazeDisplay") -> bool:
        if self.pad is None or self.painter is None:
            return True
        self.pad.move(self.prompt_row + 1, 0)
        self.pad.clrtoeol()
        self.scroll_to_prompt()
        user_input = self.get_user_input()
        if user_input == "1":
            self.display_maze()
            self.solution_visible = False
            return True
        elif user_input == "2":
            if self.solution_visible:
                self.hide_solution()
                self.solution_visible = False
            else:
                self.show_solution()
                self.solution_visible = True
            return True
        elif user_input == "3":
            self.rotate_colors()
            return True
        elif user_input == "4":
            return False
        else:
            self.display_message("Invalid choice!")
            self.pad.move(self.prompt_row, self.prompt_col)
            self.pad.clrtoeol()
            self.redraw()
            return True

    def run(self: "MazeDisplay") -> None:
        self.display_maze()
        while True:
            key = self.stdscr.getch()

            if key == curses.KEY_RESIZE:
                self.handle_resize()
            elif key == curses.KEY_UP:
                self.scroll_up()
            elif key == curses.KEY_DOWN:
                self.scroll_down()
            elif key == curses.KEY_LEFT:
                self.scroll_left()
            elif key == curses.KEY_RIGHT:
                self.scroll_right()
            elif key == ord("i"):
                if not self.handle_user_input():
                    break
