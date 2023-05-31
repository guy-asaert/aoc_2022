from utils import iter_lines
from collections import defaultdict


class Cave:

    def __init__(self, rock_formations):
        self._cave = defaultdict(dict)
        for rock_formation in rock_formations:
            for i in range(len(rock_formation[:-1])):
                f_x, f_y = rock_formation[i]
                t_x, t_y = rock_formation[i + 1]
                if f_x == t_x:
                    f_y, t_y = sorted([f_y, t_y])
                    for y in range(f_y, t_y + 1):
                        self._cave[y][f_x] = '#'
                else:
                    f_x, t_x = sorted([f_x, t_x])
                    for x in range(f_x, t_x + 1):
                        self._cave[f_y][x] = '#'

    @property
    def cave_layout(self):
        return self._cave

    def __repr__(self):
        pass


def part1():

    rock_formations = []
    for line in iter_lines(__file__, '_sample.txt'):
        rock = []
        for coord in line.split(' -> '):
            rock.append([int(c) for c in coord.split(',')])
        rock_formations.append(rock)

    cave = Cave(rock_formations)

    # for row, row_data in enumerate(cave):
    #     if row < 10:
    #         print(','.join(row_data[490:510]))

    # now let the sand flow
    pass


if __name__ == '__main__':
    part1()
