"""
Advent of Code 2022 - Day 23
Puzzle Solution
Author: Guy
Date: 12 November 2024
"""
from collections import defaultdict, namedtuple, Counter
from utils import iter_lines

EXAMPLE_INPUT = '''....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..'''

Coords = namedtuple('Coords', 'x y')

MOVEMENTS = [ 
    ('N', 'NW', 'NE'), 
    ('S', 'SW', 'SE'), 
    ('W', 'NW', 'SW'), 
    ('E', 'NE', 'SE'),]

OFFSETS = { 'N': (0, -1),
            'NE': (1, -1),
            'E': (1, 0),
            'SE': (1, 1),
            'S': (0, 1),
            'SW': (-1, 1),
            'W': (-1, 0),
            'NW': (-1, -1),
            }

def print_grid(elves_coordinates):
    min_x = min([coords.x for coords in elves_coordinates])
    max_x = max([coords.x for coords in elves_coordinates])
    min_y = min([coords.y for coords in elves_coordinates])
    max_y = max([coords.y for coords in elves_coordinates])
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Coords(x, y) in elves_coordinates:
                print('E', end='')
            else:
                print('.', end='')
        print()
    print()

def run():
    print("Day 23: Puzzle")

    elves_location = defaultdict(list)
    elf_id = 0

    # for y, line in enumerate(EXAMPLE_INPUT.split('\n')):
    for y, line in enumerate(iter_lines(__file__, '_puzzle.txt')):
        for x, char in enumerate(line):
            if char == '#':
                elves_location[elf_id].append(Coords(x, y))
                elf_id += 1
    
    movement_start_index = 0

    print("Initial state")
    elves_coordinates = [coords[-1] for coords in elves_location.values()]
    print_grid(elves_coordinates)

    for i in range(10):
        elves_coordinates = [coords[-1] for coords in elves_location.values()]
        
        print (f'Round {i + 1}')
        for elf_id, coords in elves_location.items():
            assert len(coords) == 1, "Too many coords for elf"
            x = coords[0].x
            y = coords[0].y

            # check if any of the adjacent spots are occupied
            adjacent_spots_free = {movement: Coords(x + offset[0], y + offset[1]) not in elves_coordinates for movement, offset in OFFSETS.items()}
            if all(adjacent_spots_free.values()): # all spots are free so elf does not move
                continue

            for i in range(4):
                movement_index = (movement_start_index + i) % 4
                free_spots = [adjacent_spots_free[movement] for movement in MOVEMENTS[movement_index]]
                if all(free_spots):
                    move_x = OFFSETS[MOVEMENTS[movement_index][0]][0] + x
                    move_y = OFFSETS[MOVEMENTS[movement_index][0]][1] + y
                    elves_location[elf_id].append(Coords(move_x, move_y))
                    break

        # find overlapping elves
        overlapping_elves = Counter([coords[-1] for coords in elves_location.values()])
        
        for elf_id in elves_location.keys():
            if overlapping_elves[elves_location[elf_id][-1]] > 1:
                assert len(elves_location[elf_id]) == 2, "This elf did not move"
                elves_location[elf_id].pop(1)
            elif len(elves_location[elf_id]) == 2:
                elves_location[elf_id].pop(0)

            assert len(elves_location[elf_id]) == 1, "Should only have one coord"

        print_grid(elves_coordinates)
        movement_start_index += 1
        movement_start_index %= 4

    # print the elves location
    elves_coordinates = [coords[-1] for coords in elves_location.values()]
    min_x = min([coords.x for coords in elves_coordinates])
    max_x = max([coords.x for coords in elves_coordinates])
    min_y = min([coords.y for coords in elves_coordinates])
    max_y = max([coords.y for coords in elves_coordinates])
    # for y in range(min_y, max_y + 1):
    #     for x in range(min_x, max_x + 1):
    #         if Coords(x, y) not in elves_coordinates:
    #             empty_ground_tiles += 1

    print(f'Empty ground tiles: {(max_x - min_x + 1) * (max_y - min_y + 1) - len(elves_coordinates)}')
    print(f'4164 is too high :-(')

if __name__ == "__main__":
    run()
