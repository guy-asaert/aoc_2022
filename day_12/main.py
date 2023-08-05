from utils import read_lines
from queue import PriorityQueue


class Elevation:
    def __init__(self, height, row, column):
        self.visited = False
        self.height = height
        self.row = row
        self.column = column
        self.distance = 0


def part1():
    grid_text = read_lines(__file__, sample=True)

    processing_queue = PriorityQueue()
    grid = []
    start = None
    end = None
    for r, row in enumerate(grid_text):
        row_elevation = []
        for c, e in enumerate(row):
            if e == 'S':
                start = (r, c)
                row_elevation.append(Elevation('a'))
            elif e == 'E':
                end = (r, c)
                row_elevation.append(Elevation('z'))
            else:
                row_elevation.append(Elevation(c))

        grid.append(row_elevation)

    start_loc = grid[start[0]][start[1]]
    processing_queue.put((start_loc.height, start_loc))

    while not processing_queue.empty():
        process_node = processing_queue.get()
        if process_node.column > 0:
            left_node = grid[process_node.row][process_node.column-1]
            if left_node.height <= process_node.height + 1:
                if not left_node.visited:
                    left_node.visited = True
                    left_node.distance = process_node.distance + 1
                    processing_queue.put(())




if __name__ == '__main__':
    part1()