"""
Advent of Code 2022 - Day 22
Puzzle Solution
Author: Guy
Date: 7 November 2024
"""

import re
from collections import namedtuple
from utils import iter_lines
import coverage
import coverage.html

XEdge = namedtuple('XEdge', ['left', 'right'])
YEdge = namedtuple('YEdge', ['top', 'bottom'])
MapDetails = namedtuple('MapDetails', ['material', 'face'])

PUZZLE_INPUT_SAMPLE = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5'''

# PANEL_SIZE = 4 # for the sample - 50 for the puzzle input
PANEL_SIZE = 50 # for the puzzle input

# WRAPPING_DETAILS = {
#     ('E', 0): ('W', 2),
#     ('E', 1): ('S', 3),
#     ('E', 2): ('W', 0),
#     ('E', 3): ('N', 1),
#     ('W', 0): ('S', 1),
#     ('W', 1): ('N', 3),
#     ('W', 2): ('N', 1),
#     ('W', 3): ('E', 0),
#     ('N', 0): ('S', 2),
#     ('N', 1): ('E', 0),
#     ('N', 2): ('S', 0),
#     ('N', 3): ('W', 1),
#     ('S', 0): ('N', 2),
#     ('S', 1): ('E', 2),
#     ('S', 2): ('N', 0),
#     ('S', 3): ('E', 1)
# }

WRAPPING_DETAILS = {
    ('E', 0): ('W', 2, True),
    ('E', 1): ('N', 2, False),
    ('E', 2): ('W', 0, True),
    ('E', 3): ('N', 1, False),

    ('W', 0): ('E', 2, True),
    ('W', 1): ('S', 0, False),
    ('W', 2): ('E', 0, True),
    ('W', 3): ('S', 1, False),

    ('N', 0): ('E', 1, False),
    ('N', 1): ('E', 3, False),
    ('N', 2): ('N', 0, False),

    ('S', 0): ('S', 2, False),
    ('S', 1): ('W', 3, False),
    ('S', 2): ('W', 1, False),
}

TURN_RIGHT_MAP = {
    'E': 'S',
    'S': 'W',
    'W': 'N',
    'N': 'E'
    }

TURN_LEFT_MAP = {
    'E': 'N',
    'N': 'W',
    'W': 'S',
    'S': 'E'
    }

FACING_MAP = { 'E': 0, 'S': 1, 'W': 2, 'N': 3 }

def first_non_matching_char(s, char):
    """
    Find the first character in the string `s` that is not `char`.

    :param s: The input string.
    :param char: The character to be skipped.
    :return: The first non-matching character or None if all characters match.
    """
    for i, c in enumerate(s):
        if c != char:
            return i
    return -1

def wrap_around_cube(pos_x, pos_y, direction, x_edges, y_edges):
    if direction == 'E' or direction == 'W':
        y_panel = pos_y // PANEL_SIZE
        offset = pos_y % PANEL_SIZE
        wrap_direction, wrap_panel, swap = WRAPPING_DETAILS[(direction, y_panel)]
    elif direction == 'N' or direction == 'S':
        x_panel = pos_x // PANEL_SIZE
        offset = pos_x % PANEL_SIZE
        wrap_direction, wrap_panel, swap = WRAPPING_DETAILS[(direction, x_panel)]
    else:
        raise ValueError(f'Unknown direction: {direction}')

    if wrap_direction == 'E':
        next_pos_y = wrap_panel * PANEL_SIZE + (offset if not swap else (PANEL_SIZE - 1 - offset))
        next_pos_x = x_edges[next_pos_y].left
    elif wrap_direction == 'W':
        next_pos_y = wrap_panel * PANEL_SIZE + (offset if not swap else (PANEL_SIZE - 1 - offset))
        next_pos_x = x_edges[next_pos_y].right
    elif wrap_direction == 'N':
        next_pos_x = wrap_panel * PANEL_SIZE + (offset if not swap else (PANEL_SIZE - 1 - offset))
        next_pos_y = y_edges[next_pos_x].bottom
    elif wrap_direction == 'S':
        next_pos_x = wrap_panel * PANEL_SIZE + (offset if not swap else (PANEL_SIZE - 1 - offset))
        next_pos_y = y_edges[next_pos_x].top

    print(f'Wrap around from ({pos_x}, {pos_y}) to ({next_pos_x}, {next_pos_y})')
    return wrap_direction, next_pos_x, next_pos_y

def run():
    # Start coverage measurement
    # cov = coverage.Coverage()
    # cov.start()

    # rows = PUZZLE_INPUT_SAMPLE.split('\n')
    rows = list(iter_lines(__file__, '_puzzle.txt')) # PUZZLE_INPUT_SAMPLE.split('\n')
    grid = []
    for row_number, row in enumerate(rows):
        if row_number < len(rows) - 2:
            grid.append(list(row))

    row_length = max([len(row) for row in grid])
    for row in grid:
        row.extend([' ' for _ in range(row_length - len(row))])

    x_edges = []
    for row in grid:
        x_edges.append(XEdge(first_non_matching_char(row, ' '), row_length - first_non_matching_char(reversed(row), ' ') - 1))
    
    y_edges = []
    for column_index in range(row_length):
        row = 0
        while grid[row][column_index] == ' ':
            row += 1
        min_y = row
        while row < len(grid) and grid[row][column_index] != ' ':
            row += 1
        y_edges.append(YEdge(min_y, row - 1))    
    pass    

    pos_y = 0
    pos_x = grid[0].index('.')
    direction = 'E'
    instructions = rows[-1]
    match_instructions = re.compile(r'(\d+)([RL]?)')
    for match in match_instructions.finditer(instructions):
        distance, turn_to = match.groups()[0], match.groups()[1]
        distance = int(distance)
        print(f"PRE: Move {distance} steps. Current position: ({pos_x}, {pos_y}). Current direction: {direction}")

        for i in range(distance):
            if direction == 'E': # increment x
                next_pos_x = pos_x + 1
                next_pos_y = pos_y
                next_direction = direction
                if next_pos_x >= row_length or grid[next_pos_y][next_pos_x] == ' ':
                    # wrap around
                    next_direction, next_pos_x, next_pos_y = wrap_around_cube(pos_x, pos_y, direction, x_edges, y_edges)
            elif direction == 'W': # decrement x
                next_pos_x = pos_x - 1
                next_pos_y = pos_y
                next_direction = direction
                if next_pos_x < 0 or grid[next_pos_y][next_pos_x] == ' ':
                    # wrap around
                    next_direction, next_pos_x, next_pos_y = wrap_around_cube(pos_x, pos_y, direction, x_edges, y_edges)
            elif direction == 'N': # decrement y
                next_pos_x = pos_x
                next_pos_y = pos_y - 1
                next_direction = direction
                if next_pos_y < 0 or grid[next_pos_y][next_pos_x] == ' ':
                    # wrap around
                    next_direction, next_pos_x, next_pos_y = wrap_around_cube(pos_x, pos_y, direction, x_edges, y_edges)
            elif direction == 'S': # increment y
                next_pos_x = pos_x
                next_pos_y = pos_y + 1
                next_direction = direction
                if next_pos_y >= len(grid) or grid[next_pos_y][next_pos_x] == ' ':
                    # wrap around
                    next_direction, next_pos_x, next_pos_y = wrap_around_cube(pos_x, pos_y, direction, x_edges, y_edges)
            else:
                raise ValueError(f'Unknown direction: {direction}')

            if grid[next_pos_y][next_pos_x] == '#':
                print(f'Hit a wall at ({next_pos_x}, {next_pos_y})')
                break # hit a wall so do nothing
            pos_x = next_pos_x
            pos_y = next_pos_y
            direction = next_direction

        print(f"POST: Move {distance} steps. New position: ({pos_x}, {pos_y}). New direction: {direction}")
        if turn_to == 'R':
            direction = TURN_RIGHT_MAP[direction]
        elif turn_to == 'L':
            direction = TURN_LEFT_MAP[direction]
        elif turn_to != '':
            raise ValueError(f'Unknown turn direction: {turn_to}')
        print(f'Turn {turn_to}. New direction: {direction}')

    print(f'Password: {1000 * (pos_y + 1) + 4 * (pos_x + 1) + FACING_MAP[direction]}')
    print(f'115040 is too low :-(')
    print(f'177092 is too high :-(')

    # Stop coverage measurement and save report
    # cov.stop()
    # cov.save()
    # cov.html_report(directory='coverage_html_report')
    # print("Coverage report generated in 'coverage_html_report' directory.")

if __name__ == "__main__":
    run()
