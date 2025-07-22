import random
import tkinter as tk
from tkinter import messagebox


CELL_SIZE = 32


class BlindsortApp:
    def __init__(self, root):
        self.root = root
        root.title('BlindSort')

        frame_top = tk.Frame(root)
        frame_top.pack(pady=5)
        tk.Label(frame_top, text='Anzahl:').pack(side='left', padx=5)
        self.entry = tk.Entry(frame_top, width=10)
        self.entry.pack(side='left', padx=5)
        self.entry.insert(0, '3')
        tk.Button(frame_top, text='Erstellen', command=self.on_create_click).pack(side='left', padx=5)

        self.data_canvas = tk.Canvas(root, width=450, height=CELL_SIZE)
        self.data_canvas.pack(pady=10)
        self.data_canvas.bind('<Button-1>', self.on_canvas_click)

        frame_bottom = tk.Frame(root)
        frame_bottom.pack(pady=5)
        tk.Button(frame_bottom, text='Tauschen', command=self.on_swap_click).pack(side='left', padx=5)
        self.preview_canvas = tk.Canvas(frame_bottom, width=CELL_SIZE, height=CELL_SIZE)
        self.preview_canvas.pack(side='left', pady=5)
        tk.Button(frame_bottom, text='Info', command=self.on_info_click).pack(side='left', padx=5)
        tk.Button(frame_bottom, text='Abschließen', command=self.on_complete_click).pack(side='left', padx=5)

        self.on_create_click()

    def on_create_click(self) -> None:
        try:
            value = int(self.entry.get())
            assert(value >= 2)
            assert(value <= 12)
        except (ValueError, AssertionError):
            messagebox.showerror('Fehler', 'Bitte eine Anzahl zwischen 2 und 12 eingeben.')
            return
        
        self.data = [random.randrange(value ** 2) for _ in range(value)]
        self.index1 = -1
        self.index2 = -1
        self.num_comp = 0
        self.num_swap = 0

        self.redraw()
    
    def redraw(self) -> None:
        self.data_canvas.delete('all')
        for i in range(len(self.data)):
            x1 = i * CELL_SIZE + i * CELL_SIZE // 8
            y1 = 0
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            color = '#0000FF' if i not in [self.index1, self.index2] else '#FFFF00'
            self.data_canvas.create_rectangle(x1, y1, x2, y2, outline='#000000', fill=color)
        
        color = '#606060'
        max_index = len(self.data) - 1
        if -1 < self.index1 <= max_index and -1 < self.index2 <= max_index:
            left_index = min(self.index1, self.index2)
            right_index = max(self.index1, self.index2)
            self.num_comp += 1
            color = '#00FF00' if self.data[left_index] <= self.data[right_index] else '#FF0000'
        self.preview_canvas.create_rectangle(0, 0, CELL_SIZE, CELL_SIZE, outline='#000000', fill=color)

    def on_canvas_click(self, event: tk.Event) -> None:
        i = event.x // (CELL_SIZE + CELL_SIZE // 8)
        if self.index1 == i:
            # unselect 1st
            self.index1 = -1
        elif self.index2 == i:
            # unselect 2nd
            self.index2 = -1
        elif self.index1 == -1:
            # select as 1st
            self.index1 = i
        elif self.index2 == -1:
            # select as 2nd
            self.index2 = i
        else:
            # replace
            self.index1 = self.index2
            self.index2 = i
        
        self.redraw()
    
    def on_swap_click(self) -> None:
        if self.index1 == -1 or self.index2 == -1:
            messagebox.showerror('Fehler', 'Wähle zuerst zwei Elemente und klicke dann auf Tauschen.')
            return

        tmp = self.data[self.index1]
        self.data[self.index1] = self.data[self.index2]
        self.data[self.index2] = tmp
        self.index1 = -1
        self.index2 = -1
        self.num_swap += 1

        self.redraw()

    def on_info_click(self) -> None:
        messagebox.showinfo('Info', 'Sortiere die Elemente durch Tauschen. Ist die Ausgabe grün, dann sind die zwei gewählten Elemente in der richtigen Reihenfolge.')

    def on_complete_click(self) -> None:
        check = True
        for i in range(len(self.data) - 1):
            if self.data[i] > self.data[i+1]:
                check = False
                break
        
        if not check:
            messagebox.showwarning('Unvollständig', 'Nein, das ist noch nicht sortiert!')
        else:
            messagebox.showinfo('Abgeschlossen', f'Okay, das waren jetzt {self.num_comp} Vergleich- und {self.num_swap} Tauschoperationen.')


def main() -> None:
    root = tk.Tk()
    app = BlindsortApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
