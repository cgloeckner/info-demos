import time
import sys
import tkinter as tk

from maze import *
from shared.grid import TkGrid, TkShape


class MazeDrawer(TkGrid):
    """Zeichnet Labyrinth"""

    def __init__(self, root: tk.Tk, maze: Maze, delay: int):
        super().__init__(root, maze.width, maze.height, 24)
        self.__maze = maze
        self.__delay = delay

    def get_cell_color(self, x: int, y: int, data) -> str:
        """Bestimmt Farbe eines Pixels"""
        if data.type_ == FieldType.WAY:
            if data.visited:
                return 'orange'
            return 'white'
        if data.type_ == FieldType.WALL:
            return 'black'
        if data.type_ == FieldType.START:
            return 'blue'
        if data.type_ == FieldType.FINISH:
            return 'red'
        raise ValueError(data)
    
    def __call__(self) -> None:
        """Zeichnet und delayt ggf."""
        self.draw_shapes(self.__maze.fields, shape=TkShape.RECTANGLE)

        if self.__delay > 0:
            time.sleep(self.__delay / 1000.0)


def main() -> None:
    if len(sys.argv) != 3:
        print(sys.argv)
        print('./main.py <filename.txt> <delay_in_ms>')
        raise SystemExit()

    filename = sys.argv[1]
    delay = int(sys.argv[2])

    m = Maze()
    m.load_from_file(filename)
    x, y = m.get_start_pos()

    root = tk.Tk()
    root.title('Wegsuche im Labyrinth')
    root.resizable(False, False)

    d = MazeDrawer(root, m, delay)
    search(m, x, y, True, d.__call__)
    root.mainloop()


if __name__ == '__main__':
    main()
