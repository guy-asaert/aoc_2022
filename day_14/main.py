from utils import iter_lines
from collections import defaultdict


ROCK = '#'
SAND = 'o'
AIR = '.'


class Cave:

    def __init__(self, rock_formations, floor=False):
        self._cave = defaultdict(dict)
        self._floor = floor
        for rock_formation in rock_formations:
            for i in range(len(rock_formation[:-1])):
                f_x, f_y = rock_formation[i]
                t_x, t_y = rock_formation[i + 1]
                if f_x == t_x:
                    f_y, t_y = sorted([f_y, t_y])
                    for y in range(f_y, t_y + 1):
                        self._cave[y][f_x] = ROCK
                else:
                    f_x, t_x = sorted([f_x, t_x])
                    for x in range(f_x, t_x + 1):
                        self._cave[f_y][x] = ROCK
        self._floor_level = self.max_y + 2

    def drop_sand(self, x_start, y_start):

        add_more_sand = True
        x = x_start
        y = y_start

        sand_units = 0
        while add_more_sand:
            x = x_start
            y = y_start

            if self.at(x, y) == SAND:
                return sand_units

            self._cave[y][x] = SAND

            dropping = True
            while dropping:
                new_y = y + 1
                if not self._floor and new_y > self.max_y:  # sand flowing down
                    return sand_units

                if self.at(x, new_y) == AIR:
                    self._cave[y][x] = AIR
                    y = new_y
                    self._cave[y][x] = SAND
                elif self.at(x-1, new_y) == AIR:
                    self._cave[y][x] = AIR
                    x -= 1
                    y = new_y
                    self._cave[y][x] = SAND
                elif self.at(x+1, new_y) == AIR:
                    self._cave[y][x] = AIR
                    x += 1
                    y = new_y
                    self._cave[y][x] = SAND
                else:  # come to rest
                    dropping = False
            sand_units += 1

        raise RuntimeError('Invalid execution path')

    def at(self, x, y):
        if self._floor and y == self._floor_level:
            return ROCK

        return self._cave.get(y, dict()).get(x, AIR)

    @property
    def cave_layout(self):
        return self._cave

    @property
    def min_x(self):
        return min(min(d.keys()) for d in self._cave.values())

    @property
    def max_x(self):
        return max(max(d.keys()) for d in self._cave.values())

    @property
    def min_y(self):
        return min(self._cave.keys())

    @property
    def max_y(self):
        return max(self._cave.keys())

    def __repr__(self):
        image = ''
        for y in range(self.min_y, self.max_y+1):
            for x in range(self.min_x, self.max_x+1):
                image += self.at(x, y)
            image += '\n'
        return image


def solve():

    rock_formations = []
    for line in iter_lines(__file__, '_puzzle.txt'):
        rock = []
        for coord in line.split(' -> '):
            rock.append([int(c) for c in coord.split(',')])
        rock_formations.append(rock)

    cave = Cave(rock_formations)
    print(cave.drop_sand(500, 0))

    cave = Cave(rock_formations, floor=True)
    print(cave.drop_sand(500, 0))
    # print(cave)


if __name__ == '__main__':
    solve()
