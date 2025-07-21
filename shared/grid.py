import tkinter as tk

from enum import Enum
from typing import Callable, Any
from abc import ABC, abstractmethod

class TkShape(Enum):
    RECTANGLE = 0
    OVAL = 1
    LINE = 2

class TkGrid(ABC):
    """Zeichnet Raster mittels Turtle/Tkinter"""

    def __init__(self, root: tk.Tk, width: int, height: int, cell_size: int):
        """Erzeugt Fenster und bereitet Zeichnen für w x h Raster mit bestimmter Zellengröße vor"""
        self.__width = width
        self.__height = height
        self.__cell_size = cell_size
        self.__shape_data = [(0, 0, 0, 0, '') for _ in range(width * height)]

        self.__canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
        self.__canvas.pack()

    @abstractmethod
    def get_cell_color(self, x: int, y: int, data) -> str:
        ...

    def __get_shape_callable(self, shape: TkShape) -> Callable[..., Any]:
        if shape == TkShape.RECTANGLE:
            return self.__canvas.create_rectangle
        
        if shape == TkShape.OVAL:
            return self.__canvas.create_oval
        
        if shape == TkShape.LINE:
            return self.__canvas.create_line

        raise ValueError(f'{shape} is no supported shape.')

    def draw_shapes(self, grid_data: list, shape: TkShape) -> None:
        """Zeichnet alle Zellen des gegebenen Rasters"""
        assert(self.__width * self.__height == len(grid_data))
        self.__canvas.delete('all')
        shape_callable = self.__get_shape_callable(shape)

        index = 0
        for y in range(self.__height):
            y1 = y * self.__cell_size
            y2 = (y+1) * self.__cell_size
            
            for x in range(self.__width):
                x1 = x * self.__cell_size
                x2 = (x+1) * self.__cell_size
                c = self.get_cell_color(x, y, grid_data[index])
                self.__shape_data[index] = (x1, y1, x2, y2, c)
                index += 1

        for x1, y1, x2, y2, c in self.__shape_data:
            shape_callable(x1, y1, x2, y2, outline=c, fill=c)
        
        self.__canvas.update()
