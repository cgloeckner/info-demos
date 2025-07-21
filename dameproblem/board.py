from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int
    has_piece: bool = False


class Board:
    def __init__(self, size: int):
        """Erzeugt quadratisches Brett ohne Steine"""
        self.size = size
        self.cells = [Cell(x, y) for y in range(size) for x in range(size)]

    def get_index(self, x: int, y: int) -> int:
        """Berechnet Index aus Koordinaten"""
        return y * self.size + x

    def has(self, x: int, y: int) -> bool:
        """Prüft ob Koordinaten gültig sind"""
        return x >= 0 and y >= 0 and x < self.size and y < self.size

    def get(self, x: int, y: int) -> Cell:
        """Fragt ab, ob Dame auf Koordinaten steht (True = Dame dort) - oder ggf. ValueError"""
        if not self.has(x, y):
            raise ValueError(f'Invalid position ({x}|{y}) for board {self.size}x{self.size}')
        
        index = self.get_index(x, y)
        return self.cells[index]
    
    def set(self, x: int, y: int, has_piece: bool) -> None:
        """Setzt bzw. nimmt Dame vom Feld (True = Dame dort)"""
        index = self.get_index(x, y)
        self.cells[index].has_piece = has_piece

    def search_conflicts(self, x: int, y: int) -> list[tuple[int, int]]:
        """Prüft eine Position und liefert eine Liste von Koordinaten, wo problematische Damen stehen"""
        conflicts = []

        for i in range(self.size):
            # Zeile
            if i != y and self.get(x, i).has_piece:
                conflicts.append((x, i))
            # Spalte
            if i != x and self.get(i, y).has_piece:
                conflicts.append((i, y))

        for delta in range(-self.size, self.size+1):
            # Diagonale (tl;br)
            x_ = x + delta
            y_ = y + delta
            if self.has(x_, y_) and self.get(x_, y_).has_piece:
                conflicts.append((x_, y_))
            # Diagonale (bl; tr)
            y_ = y - delta
            if self.has(x_, y_) and self.get(x_, y_).has_piece:
                conflicts.append((x_, y_))

        return conflicts
