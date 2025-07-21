import tkinter as tk
from typing import Callable

from shared.automata import State, StateMachine

def on_button_click(entry: tk.Entry, test: Callable) -> None:
    word = entry.get()
    color = '#FF0000'
    if test(word):
        color = '#00AA00'
    
    entry.winfo_toplevel().configure(bg=color)


def on_entry_type(event):
    event.widget.winfo_toplevel().configure(bg="lightgrey")


def main() -> None:
    fsm = StateMachine()

    states = [fsm.add(f'#{i}') for i in range(7)]

    for i in range(ord('a'), ord('z')+1):
        states[0].link(chr(i), states[1])
        states[1].link(chr(i), states[1])
        states[2].link(chr(i), states[3])
        states[3].link(chr(i), states[3])
        states[4].link(chr(i), states[5])
        states[5].link(chr(i), states[6])
        states[6].link(chr(i), states[6])

    for i in range(ord('A'), ord('Z')+1):
        states[0].link(chr(i), states[1])
        states[1].link(chr(i), states[1])
        states[2].link(chr(i), states[3])
        states[3].link(chr(i), states[3])
        states[4].link(chr(i), states[5])
        states[5].link(chr(i), states[6])
        states[6].link(chr(i), states[6])

    for i in range(10):
        states[0].link(chr(ord('0') + i), states[1])
        states[1].link(chr(ord('0') + i), states[1])
        states[2].link(chr(ord('0') + i), states[3])
        states[3].link(chr(ord('0') + i), states[3])
        states[4].link(chr(ord('0') + i), states[5])
        states[5].link(chr(ord('0') + i), states[6])
        states[6].link(chr(ord('0') + i), states[6])

    states[1].link('.', states[0])
    states[1].link('@', states[2])
    states[3].link('.', states[4])
    states[5].link('.', states[4])
    states[6].link('.', states[4])

    states[6].final = True
    test_word = lambda word: fsm(states[0], word)

    root = tk.Tk()
    root.title('Akzeptor')

    entry = tk.Entry(root, width=40)
    entry.pack(pady=10)
    entry.bind('<Key>', on_entry_type)

    button = tk.Button(root, text='Prüfen', command=lambda: on_button_click(entry, test_word))
    button.pack(pady=5)

    root.mainloop()


if __name__ == '__main__':
    main()
