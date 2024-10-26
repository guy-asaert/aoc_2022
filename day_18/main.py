import sys
from collections import namedtuple
from itertools import product
# from utils import iter_lines

PUZZLE_SAMPLE = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def solve():

    outside_walls = None
    cubes = []

    unique_walls = list()

    touching_walls = 0
    for row in PUZZLE_SAMPLE.split('\n'):
    # for row in iter_lines(__file__, '_puzzle.txt'):
        x, y, z = map(int, row.split(','))

        wall1 = set(product([x - 1],    [y - 1, y], [z - 1, z]))
        wall2 = set(product([x],        [y - 1, y], [z - 1, z]))
        wall3 = set(product([x - 1, x], [y - 1],    [z - 1, z]))
        wall4 = set(product([x - 1, x], [y],        [z - 1, z]))
        wall5 = set(product([x - 1, x], [y - 1, y], [z - 1]))
        wall6 = set(product([x - 1, x], [y - 1, y], [z]))

        cube_walls = [wall1, wall2, wall3, wall4, wall5, wall6]

        for cube_wall in cube_walls:
            if cube_wall not in unique_walls:
                unique_walls.append(cube_wall)
            else:
                touching_walls += 1
                unique_walls.remove(cube_wall)

    print(len(unique_walls))

    # find all the walls that are on the outside
    start_wall = None
    curr_min_x = sys.maxsize
    for process_this_wall in unique_walls:
        min_x = min(process_this_wall, key=lambda x: x[0])[0]
        if min_x < curr_min_x:
            start_wall = process_this_wall
            curr_min_x = min_x

    process_walls = [start_wall]
    unique_walls.remove(start_wall)
    outside_walls = list()

    while process_walls:
        process_this_wall = process_walls.pop(0)
        outside_walls.append(process_this_wall)

        # find all the adjacent walls
        adjacent_walls = []
        for other_wall in unique_walls:
            if process_this_wall == other_wall:
                continue

            if len(process_this_wall.intersection(other_wall)) == 2:
                adjacent_walls.append(other_wall)
        
        for adjacent_wall in adjacent_walls:
            unique_walls.remove(adjacent_wall)
            process_walls.append(adjacent_wall)

    print(len(outside_walls))

if __name__ == '__main__':
    solve()
