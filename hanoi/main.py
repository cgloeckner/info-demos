import sys
import hashlib
import tkinter as tk
from tkinter import messagebox

from tower import Tower


MAX_DISC_WIDTH = 200
DISC_HEIGHT = 25
ROD_WIDTH = 10
ROD_HEIGHT = 200


def int_to_color(n: int) -> str:
    h = hashlib.md5(str(n).encode()).hexdigest()
    
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    
    return f"#{r:02X}{g:02X}{b:02X}"


class HanoiApp:
    def __init__(self, root: tk.Tk, num_discs: int):
        self.root = root
        root.title('Türme von Hanoi')

        frame = tk.Frame(root)
        frame.pack(pady=5)
        self.canvas_list = [tk.Canvas(frame, width=MAX_DISC_WIDTH, height=ROD_HEIGHT) for _ in range(3)]
        for c in self.canvas_list:
            c.pack(side='left', pady=10)
            c.bind('<Button-1>', self.on_canvas_click)

        self.selected_column = -1
        self.populate(num_discs)
        self.redraw()

    def populate(self, num_discs: int) -> None:
        self.tower_list = [Tower() for _ in range(3)]
        delta_width = MAX_DISC_WIDTH // num_discs

        for i in range(num_discs):
            disc_width = (num_discs - i) * delta_width
            self.tower_list[0].push(disc_width)

    def redraw(self) -> None:
        for c in self.canvas_list:
            c.config(bg='#FFFFFF')
            c.delete('all')
            x1 = MAX_DISC_WIDTH // 2 - ROD_WIDTH // 2
            y1 = 0
            x2 = x1 + ROD_WIDTH
            y2 = ROD_HEIGHT
            c.create_rectangle(x1, y1, x2, y2, fill='#000000')
        
        if self.selected_column != -1:
            self.canvas_list[self.selected_column].config(bg='#FFFF00')

        for c, t in zip(self.canvas_list, self.tower_list):
            y1 = ROD_HEIGHT
            for s in t.disc_sizes:
                x1 = MAX_DISC_WIDTH // 2 - s // 2
                x2 = x1 + s
                y2 = y1 - DISC_HEIGHT
                c.create_rectangle(x1, y1, x2, y2, fill=int_to_color(s))
                y1 = y2

    def on_canvas_click(self, event: tk.Event) -> None:
        col = [i for i, c in enumerate(self.canvas_list) if event.widget == c][0]
        
        if self.selected_column == -1:
            self.selected_column = col
        else:
            try:
                size = self.tower_list[self.selected_column].pop()
            except ValueError as error:
                size = 0
                messagebox.showinfo('Fehler', str(error))
            
            if size > 0:
                try:
                    self.tower_list[col].push(size)
                except ValueError as error:
                    self.tower_list[self.selected_column].push(size)
                    messagebox.showinfo('Fehler', str(error))

            self.selected_column = -1
        
        self.redraw()
        
    def on_info_click(self) -> None:
        messagebox.showinfo('Info', 'Sortiere die Elemente durch Tauschen. Ist die Ausgabe grün, dann sind die zwei gewählten Elemente in der richtigen Reihenfolge.')


def main() -> None:
    if len(sys.argv) != 2:
        print(sys.argv)
        print('./main.py <number_of_discs>')
        raise SystemExit()

    num_discs = int(sys.argv[1])
    assert(1 <= num_discs <= 7)

    root = tk.Tk()
    app = HanoiApp(root, num_discs)
    root.mainloop()


if __name__ == '__main__':
    main()
