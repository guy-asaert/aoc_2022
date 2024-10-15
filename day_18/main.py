
from utils import iter_lines

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
    blocks = []

    # for row in PUZZLE_SAMPLE.split('\n'):
    for row in iter_lines(__file__, '_puzzle.txt'):
        x, y, z = map(lambda v: 2 * int(v), row.split(','))
        blocks.append((x, y, z))
        walls = set([
                (x - 2, y - 1, z - 1),
                (x,     y - 1, z - 1),
                (x - 1, y - 2, z - 1),
                (x - 1, y,     z - 1),
                (x - 1, y - 1, z - 2),
                (x - 1, y - 1, z),
            ])

        if not outside_walls:
            outside_walls = walls
        else:
            outside_walls.symmetric_difference_update(walls)
    print(len(outside_walls))

    # to find trapped water we need to check all cubes inside the walls and if the symetric difference removes size walls
    
    min_x = min([x for x, _, _ in outside_walls])
    max_x = max([x for x, _, _ in outside_walls])
    min_y = min([y for _, y, _ in outside_walls])
    max_y = max([y for _, y, _ in outside_walls])
    min_z = min([z for _, _, z in outside_walls])
    max_z = max([z for _, _, z in outside_walls])

    trapped_water = 0
    trapped_blocks_walls = None
    for x in range(min_x, max_x + 1):
        x *= 2
        for y in range(min_y, max_y + 1):
            y *= 2
            for z in range(min_z, max_z + 1):
                z *= 2
                block_walls = set([
                        (x - 2, y - 1, z - 1),
                        (x,     y - 1, z - 1),
                        (x - 1, y - 2, z - 1),
                        (x - 1, y,     z - 1),
                        (x - 1, y - 1, z - 2),
                        (x - 1, y - 1, z),
                    ])
                matching_walls = outside_walls.intersection(block_walls)
                if len(matching_walls) == 6:
                    if (x, y, z) not in blocks:
                        trapped_water += 1
                        if trapped_blocks_walls is None:
                            trapped_blocks_walls = block_walls
                        else:
                            trapped_blocks_walls.symmetric_difference_update(block_walls)

    print(len(outside_walls) - len(trapped_blocks_walls))

if __name__ == '__main__':
    solve()
