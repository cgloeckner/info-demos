#!/bin/python3

import random
import tkinter as tk


def generate(start: str, width: int) -> str:
    return chr(ord(start) + random.randrange(width))

def symbol() -> str:
    n = random.randrange(10)
    if n <= 5:
        return generate('a', 26)
    if n == 6:
        return generate('A', 26)
    if n == 7:
        return generate('0', 10)
    else:
        return random.choice('$§!_')

def symbol_series() -> str:
    sym = ''.join(symbol() for _ in range(5))
    
    if random.randrange(5) > 2:
        sym += symbol_series()
    
    return sym

def upper_series() -> str:
    n = random.randrange(10)
    if n == 0:
        return generate('A', 26)
    if n <= 4:
        return symbol_series() + generate('A', 26)
    else:
        return generate('A', 26) + symbol_series()

def number_series() -> str:
    n = random.randrange(9)
    if n == 0:
        return generate('0', 10)
    if n <= 4:
        return symbol_series() + generate('0', 10)
    else:
        return generate('0', 10) + symbol_series()

def secret() -> str:
    if random.randrange(2) == 0:
        return upper_series() + number_series()
    else:
        return number_series() + upper_series()


def on_button_click(label: tk.Label) -> None:
    label.config(text=secret())


def main() -> None:
    root = tk.Tk()
    root.title('Grammatik')
    root.minsize(400, 1)

    label = tk.Label(root, text='')
    label.pack(pady=10)

    button = tk.Button(root, text='Erzeugen', command=lambda: on_button_click(label))
    button.pack(pady=5)

    root.mainloop()


if __name__ == '__main__':
    main()
