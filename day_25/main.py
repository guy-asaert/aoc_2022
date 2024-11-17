"""
Advent of Code 2022 - Day 23
Puzzle Solution
Author: Guy
Date: 12 November 2024
"""
from dataclasses import dataclass
from enum import Enum
from utils import iter_lines

EXAMPLE_INPUT = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122'''


dec_2_snafu_mapping = { '0': 0,
                 '1': 1,
                 '2': 2,
                 '=': -2,
                 '-': -1,}


shifted_snafu_to_dec_mapping = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2',}

def snafu_to_decimal(number: str) -> int:
    five_base = 1
    decimal_number = 0

    while number:
        digit = number[-1]
        number = number[:-1]

        decimal_number += dec_2_snafu_mapping[digit] * five_base
        five_base *= 5

    return decimal_number


def decimal_to_snafu(number: int) -> str:
    # add 2 and convert using the shifted mapping
    snafu_number = ''

    while number:
        number +=2
        digit = (number % 5) - 2
        number //= 5

        # if digit < 0:
        #     digit += 5
        #     number += 1

        snafu_number = shifted_snafu_to_dec_mapping[digit] + snafu_number

    return snafu_number

def run():
    print("Day 25: Puzzle")

    t1 = decimal_to_snafu(3)
    t1b = snafu_to_decimal(t1)
    pass

    total_sum = 0
    # for input_number in EXAMPLE_INPUT.split('\n'):
    for input_number in iter_lines(__file__, '_puzzle.txt'):
        decimal_number = snafu_to_decimal(input_number)
        snafu_number = decimal_to_snafu(decimal_number)
        print( f'{input_number} -> {decimal_number} -> {snafu_number}')

        total_sum += decimal_number

    print(f'Total sum: {decimal_to_snafu(total_sum)}')
    

if __name__ == "__main__":
    run()
