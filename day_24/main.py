"""
Advent of Code 2022 - Day 23
Puzzle Solution
Author: Guy
Date: 12 November 2024
"""
from dataclasses import dataclass
from enum import Enum
from utils import iter_lines

EXAMPLE_INPUT = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''

EnumDirection = Enum('EnumDirection', '^ v < >')

@dataclass
class Blizzard:
    """Class representing a blizzard"""
    direction: EnumDirection
    x: int
    y: int

OFFSETS = ((0, -1), (0, 1), (-1, 0), (1, 0))


def print_grid(process_positions, blizzards, walls, columns, rows):

    return
    blizzard_for_printing = dict()
    for blizzard in blizzards:
        if (blizzard.x, blizzard.y) in blizzard_for_printing:
            if isinstance(blizzard_for_printing[(blizzard.x, blizzard.y)], str):
                blizzard_for_printing[(blizzard.x, blizzard.y)] = 2
            else:
                blizzard_for_printing[(blizzard.x, blizzard.y)] += 1
        else:
            blizzard_for_printing[(blizzard.x, blizzard.y)] = blizzard.direction.name
    
    blizzards = 0

    for y in range(rows):
        for x in range(columns):
            if (x, y) in process_positions:
                print('E', end='')
            elif (x, y) in blizzard_for_printing:
                print(blizzard_for_printing[(x, y)], end='')
                if isinstance(blizzard_for_printing[(x, y)], int):
                    blizzards += blizzard_for_printing[(x, y)]
                else:
                    blizzards += 1
            elif (x, y) in walls:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

    return blizzards


def move_blizzards(blizzards: list, columns: int, rows: int):
    for blizzard in blizzards:
        if blizzard.direction == EnumDirection['^']:
            blizzard.y -= 1
            if blizzard.y < 1:
                blizzard.y = rows - 2
        elif blizzard.direction == EnumDirection['v']:
            blizzard.y += 1
            if blizzard.y >= rows - 1:
                blizzard.y = 1
        elif blizzard.direction == EnumDirection['<']:
            blizzard.x -= 1
            if blizzard.x < 1:
                blizzard.x = columns - 2
        elif blizzard.direction == EnumDirection['>']:
            blizzard.x += 1
            if blizzard.x >= columns - 1:
                blizzard.x = 1

def run():
    print("Day 24: Puzzle")

    blizzards = list()

    columns = 0
    rows = 0
    walls = set()
    # for row, puzzle_input_row in enumerate(EXAMPLE_INPUT.split('\n')):
    for row, puzzle_input_row in enumerate(iter_lines(__file__, '_puzzle.txt')):
        columns = max(columns, len(puzzle_input_row))
        for column, cell in enumerate(puzzle_input_row):
            if cell == '#':
                walls.add((column, row))
            elif cell not in '.':
                blizzards.append(Blizzard(EnumDirection[cell], column, row))
        rows += 1
    
    target_x = columns - 2
    target_y = rows - 1
    minutes = 0

    # move_blizzards(blizzards, columns, rows)
    # blizzard_positions = set([(blizzard.x, blizzard.y) for blizzard in blizzards])

    start_position = (1, 0)
    target_positions = [(target_x, target_y), (1, 0), (target_x, target_y)]
    for target_position in target_positions:
        process_positions = [start_position]
        while process_positions:
            # blizzard_count = print_grid(process_positions, blizzards, columns, rows)
            # assert blizzard_count == len(blizzards), (blizzard_count, len(blizzards))

            minutes += 1
            move_blizzards(blizzards, columns, rows)
            next_blizzard_positions = set([(blizzard.x, blizzard.y) for blizzard in blizzards])
            
            next_process_positions = set()
            # move ourselves
            while process_positions:
                x, y = process_positions.pop()

                if (x, y) not in next_blizzard_positions:
                    next_process_positions.add((x, y))

                for offset in OFFSETS:
                    x_new = x + offset[0]
                    y_new = y + offset[1]
                    if y_new < 0 or y_new == rows or (x_new, y_new) in walls:
                        continue
                    if (x_new, y_new) in next_blizzard_positions:
                        continue
                    next_process_positions.add((x_new, y_new))


                # if (x, y) not in next_blizzard_positions:
                #     next_process_positions.add((x, y)) # stay in the same position
                # if x > 0 and (x - 1, y) not in next_blizzard_positions:
                #     next_process_positions.add((x - 1, y)) # move left
                # if y > 0 and (x, y - 1) not in next_blizzard_positions:
                #     next_process_positions.add((x, y - 1)) # move up
                # if x < columns - 1 and (x + 1, y) not in next_blizzard_positions:
                #     next_process_positions.add((x + 1, y)) # move right
                # if y < rows - 1 and (x, y + 1) not in next_blizzard_positions:
                #     next_process_positions.add((x, y + 1)) # move down
            
            print_grid(next_process_positions, blizzards, walls, columns, rows)

            if target_position in next_process_positions:
                print(f"Arrived at the target at {minutes} minutes")
                print_grid(next_process_positions, blizzards, walls, columns, rows)
                next_process_positions.clear()
                break

            process_positions = list(next_process_positions)
        copy_start_position = start_position
        start_position = target_position
        target_position = copy_start_position

    print(minutes) # add one to exit the maze

if __name__ == "__main__":
    run()
