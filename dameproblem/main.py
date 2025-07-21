import sys

import tkinter as tk

from board import Board
from shared.grid import TkGrid, TkShape


import turtle


class CheckeredBoard(TkGrid):
    def __init__(self, root: tk.Tk, board: Board, squaresize: int):
        super().__init__(root, board.size, board.size, squaresize)
        self.__board = board

    def get_cell_color(self, x: int, y: int, data) -> str:
        return '#000000' if (x+y) % 2 == 0 else '#FFFFFF'

    def __call__(self) -> None:
        self.draw_shapes(self.__board.cells, TkShape.RECTANGLE)
        
        padding = self._cell_size // 8
        for cell in self.__board.cells:
            if not cell.has_piece:
                continue
            x1 = cell.x * self._cell_size + padding
            y1 = cell.y * self._cell_size + padding
            x2 = (cell.x+1) * self._cell_size - padding
            y2 = (cell.y+1) * self._cell_size - padding
            color = '#DAA520'
            self._canvas.create_oval(x1, y1, x2, y2, outline=color, fill=color)

    def on_left_click(self, event: tk.Event) -> None:
        x = event.x // self._cell_size
        y = event.y // self._cell_size
        
        if self.__board.get(x, y).has_piece:
            # entfernen
            self.__board.set(x, y, False)
            self.__call__()
            return

        # testen
        conflicts = self.__board.search_conflicts(x, y)
        if len(conflicts) > 0:
            self.__call__()
            self.draw_conflicts(x, y, conflicts)
            return
        
        self.__board.set(x, y, True)
        self.__call__() 

    def draw_conflicts(self, x: int, y: int, conflicts: list[tuple[int, int]]) -> None:
        color = '#FF0000'
        callable = self._get_shape_callable(TkShape.LINE)
        x = x * self._cell_size + self._cell_size // 2
        y = y * self._cell_size + self._cell_size // 2
        for x_, y_ in conflicts:
            x2 = x_ * self._cell_size + self._cell_size // 2
            y2 = y_ * self._cell_size + self._cell_size // 2
            callable(x, y, x2, y2, fill=color, width=self._cell_size // 20)


def main() -> None:
    if len(sys.argv) < 2:
        print(sys.argv)
        print('./main.py <board_size>')
        raise SystemExit()

    board_size = int(sys.argv[1])
    b = Board(board_size)

    root = tk.Tk()
    root.title('Dameproblem')
    root.resizable(False, False)

    cb = CheckeredBoard(root, b, 640 // board_size)
    cb()

    root.bind('<Button-1>', cb.on_left_click)
    tk.mainloop()


if __name__ == '__main__':
    main()


