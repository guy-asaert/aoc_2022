"""
Advent of Code 2022 - Day 20
Puzzle Solution
Author: Guy
Date: 6 November 2024
"""

import copy
from dataclasses import dataclass
from utils import iter_lines
PUZZLE_INPUT_SAMPLE = '''1
2
-3
3
-2
0
4'''

@dataclass
class PuzzleData:
    offset: int
    processed: bool = False

    def __repr__(self):
        return f'{self.offset}'

def run():
    
    DECRYPTION_KEY = 811589153
    print(PUZZLE_INPUT_SAMPLE)
    # data = [int(x) * DECRYPTION_KEY for x in PUZZLE_INPUT_SAMPLE.split()]
    data = [int(x) * DECRYPTION_KEY for x in iter_lines(__file__, '_puzzle.txt')]

    order_location = list(range(0, len(data)))
    mix_order = copy.deepcopy(data)
    for i in range(10):
        for i, position in enumerate(order_location):
            offset = data[position]
            if offset != 0:
                data.pop(position)

                new_location = (position + offset) % len(data)

                if new_location == 0: # if moved to the front then send to the back
                    new_location = len(data)
                data[new_location:new_location] = [offset]

                order_location[i] = -1 # remove temporarily
                # shuffle everything to the right of the new location
                for j in range(len(order_location)):
                    if new_location < position:
                        if order_location[j] >= new_location and order_location[j] < position:
                            order_location[j] += 1
                    else:
                        if order_location[j] > position and order_location[j] <= new_location:
                            order_location[j] -= 1

                order_location[i] = new_location

            pass
        pass

    print(data)
    zero_position = data.index(0)
    thousendth = data[(zero_position + 1000) % len(data)]
    two_thousendth = data[(zero_position + 2000) % len(data)]
    three_thousendth = data[(zero_position + 3000) % len(data)]
    print(f'Gove coordinates: {thousendth + two_thousendth + three_thousendth}')

if __name__ == "__main__":
    run()
