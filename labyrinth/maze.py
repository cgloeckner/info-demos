from enum import Enum
from dataclasses import dataclass
from typing import Callable

class FieldType(Enum):
    WAY = 0
    WALL = 1
    START = 2
    FINISH = 3

    @staticmethod
    def char_map() -> dict[str, "FieldType"]:
        """Liefert dictionary um Symbol in FieldType zu konvertieren"""
        return {
            ' ': FieldType.WAY,
            '#': FieldType.WALL,
            'S': FieldType.START,
            'F': FieldType.FINISH
        }

    @staticmethod
    def from_string(symbol: str) -> "FieldType":
        """Konvertiert Symbol in FieldType um"""
        return FieldType.char_map()[symbol]

@dataclass
class Field:
    type_: FieldType = FieldType.WAY
    visited: bool = False
    discovered: bool = False

class Maze:
    def __init__(self):
        self.clear(0, 0)
    
    def clear(self, width: int, height: int) -> None:
        """Setzt Größe und überall freie Wege"""
        self.width = width
        self.height = height
        self.fields = [Field() for i in range(self.width * self.height)]
    
    def load_from_file(self, filename: str) -> None:
        """Lädt Aufbau aus Textdatei"""
        with open(filename, 'r') as handle:
            content = handle.read().split('\n')

        self.clear(int(content[0]), int(content[1])) 

        for y in range(self.height):
            line = content[y+2]
            for x in range(self.width):
                self.set(x, y , line[x])
        
    def get_start_pos(self) -> tuple[int, int]:
        """Sucht Startposition"""
        x = 0
        y = 0
        while not self.get(x, y).type_ == FieldType.START:
            x += 1
            if x >= self.width:
                x = 0
                y += 1
        
        return x, y

    def get_index(self, x: int, y: int) -> int:
        """Berechnet Index aus Koordinaten"""
        return y * self.width + x

    def set(self, x: int, y: int, symbol: str) -> None:
        """Ändert Labyrinth-Zelle auf ein Symbol"""
        index = self.get_index(x, y)
        self.fields[index] = Field(type_=FieldType.from_string(symbol))

    def has(self, x: int, y: int) -> bool:
        """Prüft ob Koordinaten gültig sind"""
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def get(self, x: int, y: int) -> Field:
        """Liefert Labyrinth-Zelle oder ggf. ValueError"""
        if not self.has(x, y):
            raise ValueError(f'Invalid position ({x}|{y}) for map {self.width}x{self.height}')
        
        index = self.get_index(x, y)
        return self.fields[index]

    def add_to_path(self, x: int, y: int) -> None:
        """Fügt Koordinaten in den Pfad ein"""
        field = self.get(x, y)
        field.visited = True
        field.discovered = True
    
    def drop_to_path(self, x: int, y: int) -> None:
        """Entfernt Koordinten aus dem Pfad"""
        field = self.get(x, y)
        field.visited = False


def search(maze: Maze, x: int, y: int, discovery: bool, drawer: Callable[[], None]) -> bool:
    """Sucht im Labyrinth ab der gegebenen Position und ruft den drawer nach jedem Schritt auf"""
    if not maze.has(x, y):
        return False  # cannot visit
    field = maze.get(x, y)
    if field.visited or field.type_ == FieldType.WALL:
        return False  # cannot visit
    if discovery and field.discovered:
        return False  # already visited
    
    maze.add_to_path(x, y)
    drawer()

    if field.type_ == FieldType.FINISH:
        return True

    if search(maze, x, y-1, discovery, drawer) or search(maze, x+1, y, discovery, drawer) or search(maze, x, y+1, discovery, drawer) or search(maze, x-1, y, discovery, drawer):
        return True
    
    maze.drop_to_path(x, y)
    drawer()
    return False
