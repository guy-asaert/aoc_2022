from utils import iter_lines
from collections import defaultdict
import sys


class Square:
    def __init__(self, coordinates, height, distance=sys.maxsize):
        self.coordinates = coordinates
        self.height = height
        self.distance = distance

    def __repr__(self):
        return "({}/{})-h:{}-d:{}".format(self.coordinates[0], self.coordinates[1], self.height, self.distance)


def _height(character):
    return ord(character) - ord('a')


def part1():
    start_loc = None
    end_loc = None

    unprocessed_list = []
    processed_list = []

    height_map = []
    for row, line in enumerate(iter_lines(__file__, '_puzzle.txt')):
        height_map_row = []
        for column, c in enumerate(line):
            if c == 'S':
                height_map_row.append(Square((row, column), _height('a'), 0))
                start_loc = (row, column)
            elif c == 'E':
                height_map_row.append(Square((row, column), _height('z')))
                end_loc = (row, column)
            else:
                height_map_row.append(Square((row, column), _height(c)))
            unprocessed_list.append(height_map_row[-1])
        height_map.append(height_map_row)

    # gather graph edges
    edges = defaultdict(list)
    for row, squares in enumerate(height_map):
        for column, square in enumerate(squares):
            if column > 0 and height_map[row][column-1].height <= height_map[row][column].height + 1:
                edges[height_map[row][column]].append(height_map[row][column - 1])
            if column < len(squares) - 1 and height_map[row][column+1].height <= height_map[row][column].height + 1:
                edges[height_map[row][column]].append(height_map[row][column+1])
            if row > 0 and height_map[row-1][column].height <= height_map[row][column].height + 1:
                edges[height_map[row][column]].append(height_map[row-1][column])
            if row < len(height_map) - 1 and height_map[row+1][column].height <= height_map[row][column].height + 1:
                edges[height_map[row][column]].append(height_map[row+1][column])

    distance_to_end = None
    while unprocessed_list:
        unprocessed_list.sort(key=lambda x: x.distance, reverse=True)
        shortest = unprocessed_list.pop()
        for vertex in edges[shortest]:
            if vertex.distance > shortest.distance + 1:
                vertex.distance = shortest.distance + 1

        if shortest.coordinates[0] == end_loc[0] and shortest.coordinates[1] == end_loc[1]:
            distance_to_end = shortest.distance
        processed_list.append(shortest)

    return distance_to_end


def part2():
    start_loc = None
    end_loc = None

    unprocessed_list = []
    processed_list = []

    height_map = []
    for row, line in enumerate(iter_lines(__file__, '_puzzle.txt')):
        height_map_row = []
        for column, c in enumerate(line):
            if c == 'S':
                height_map_row.append(Square((row, column), _height('a')))
                start_loc = (row, column)
            elif c == 'E':
                height_map_row.append(Square((row, column), _height('z'), 0))
                end_loc = (row, column)
            else:
                height_map_row.append(Square((row, column), _height(c)))
            unprocessed_list.append(height_map_row[-1])
        height_map.append(height_map_row)

    # gather graph edges
    edges = defaultdict(list)
    for row, squares in enumerate(height_map):
        for column, square in enumerate(squares):
            if column > 0 and height_map[row][column-1].height >= height_map[row][column].height - 1:
                edges[height_map[row][column]].append(height_map[row][column - 1])
            if column < len(squares) - 1 and height_map[row][column+1].height >= height_map[row][column].height - 1:
                edges[height_map[row][column]].append(height_map[row][column+1])
            if row > 0 and height_map[row-1][column].height >= height_map[row][column].height - 1:
                edges[height_map[row][column]].append(height_map[row-1][column])
            if row < len(height_map) - 1 and height_map[row+1][column].height >= height_map[row][column].height - 1:
                edges[height_map[row][column]].append(height_map[row+1][column])

    distance_to_end = None
    while unprocessed_list:
        unprocessed_list.sort(key=lambda x: x.distance, reverse=True)
        shortest = unprocessed_list.pop()
        for vertex in edges[shortest]:
            if vertex.distance > shortest.distance + 1:
                vertex.distance = shortest.distance + 1

        if shortest.coordinates[0] == start_loc[0] and shortest.coordinates[1] == start_loc[1]:
            distance_to_end = shortest.distance
        processed_list.append(shortest)

    shortest_path = sys.maxsize
    process_zero_height = [square for square in processed_list if square.height == 0]
    for square in process_zero_height:
        if square.height == 0 and square.distance < shortest_path:
            shortest_path = square.distance

    return shortest_path


if __name__ == '__main__':
    print(part2())
