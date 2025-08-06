#!/bin/python3

import sys

def is_operator(symbol: str) -> bool:
    return symbol in '+-*:'

def parse(word: str) -> None:
    if not word.endswith('='):
        raise ValueError('Ausdruck muss mit "=" enden.')

    expect_number = True
    for index, symbol in enumerate(word[:-1]):
        is_num = symbol.isnumeric()
        
        if expect_number and not is_num:
            raise ValueError(f'Ziffer erwartet (Stelle {index})')
        
        is_op = is_operator(symbol)
        if not is_num and not is_op:
            raise ValueError(f'Ziffer oder Operator erwartet (Stelle {index})')
        
        expect_number = is_op

def compile(word: str) -> str:
    mapping = {str(n): format(n, '04b') for n in range(10)}
    mapping.update({s: format(n+10, '04b') for n, s in enumerate('+-*:=')})
    
    return ''.join([mapping[sym] for sym in word])


def main() -> None:
    print('Taschenrechner')
    print('==============')
    word = input('Term (z.B. "2+3*4-2="): ')

    parse(word)

    code = compile(word)
    print(f'Maschinencode: {code}')


if __name__ == '__main__':
    main()
