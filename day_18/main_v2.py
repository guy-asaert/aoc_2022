from collections import namedtuple, defaultdict
from itertools import product
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


def touching_cubes(axis1, axis2, axis3):

    cubes = defaultdict(lambda: defaultdict(list))

    for x, y, z in zip(axis1, axis2, axis3):
        cubes[x][y].append(z)

    # find touching cubes
    touching_cubes = 0
    for x in cubes:
        for y in cubes[x]:
            z_coordinates = sorted(cubes[x][y])
            for i in range(1, len(z_coordinates)):
                if z_coordinates[i] - z_coordinates[i - 1] == 1:
                    touching_cubes += 1
    return touching_cubes

def is_enclosed(cube, cube_coordinates, processed_enclosed_cubes):
    """
    Determine if a group of touching enclosed cubes are fully enclosed.

    :param cube: The starting cube to check.
    :param cube_coordinates: Set of all specified cubes.
    :param enclosed_cubes: List of all potential enclosed cubes.
    :param processed_enclosed_cubes: List of already processed enclosed cubes.
    :return: True if the group of cubes is fully enclosed, False otherwise.
    """
    from collections import deque

    # Directions for moving in 3D space (x, y, z)
    directions = [
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1)
    ]

    processing_queue = deque([cube])
    visited = set()
    min_x, max_x = min(x for x, _, _ in cube_coordinates), max(x for x, _, _ in cube_coordinates)
    min_y, max_y = min(y for _, y, _ in cube_coordinates), max(y for _, y, _ in cube_coordinates)
    min_z, max_z = min(z for _, _, z in cube_coordinates), max(z for _, _, z in cube_coordinates)

    while processing_queue:
        current = processing_queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        x, y, z = current
        if x <= min_x or x >= max_x or y <= min_y or y >= max_y or z <= min_z or z >= max_z:
            return None

        for dx, dy, dz in directions:
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor not in cube_coordinates and neighbor not in visited:
                processing_queue.append(neighbor)

    processed_enclosed_cubes.extend(visited)
    return visited

def get_surfaces(cube_coordinates):
    x_coordinates, y_coordinates, z_coordinates = zip(*cube_coordinates)
    z_touching = touching_cubes(x_coordinates, y_coordinates, z_coordinates)
    x_touching = touching_cubes(y_coordinates, z_coordinates, x_coordinates)
    y_touching = touching_cubes(z_coordinates, x_coordinates, y_coordinates)

    return len(cube_coordinates) * 6 - 2 * (x_touching + y_touching + z_touching)

def solve():

    outside_walls = None

    cube_coordinates = list()
    # for row in PUZZLE_SAMPLE.split('\n'):
    for row in iter_lines(__file__, '_puzzle.txt'):
        x, y, z = map(int, row.split(','))
        cube_coordinates.append((x, y, z))
    
    total_surfaces = get_surfaces(cube_coordinates)
    print(total_surfaces)


    # look for any enlosed cubes
    all_empty_cubes = list()
    x_coordinates, y_coordinates, z_coordinates = zip(*cube_coordinates)
    
    for x in range(min(x_coordinates), max(x_coordinates) + 1):
        for y in range(min(y_coordinates), max(y_coordinates) + 1):
            for z in range(min(z_coordinates), max(z_coordinates) + 1):
                if (x, y, z) not in cube_coordinates:
                    all_empty_cubes.append((x, y, z))

    enclosed_surfaces = 0
    processed_enclosed_cubes = list()
    for enclosed_cube in all_empty_cubes:
        if enclosed_cube in processed_enclosed_cubes:
            continue
        
        enclosed_area = is_enclosed(enclosed_cube, set(cube_coordinates), processed_enclosed_cubes)
        if enclosed_area:
            enclosed_surfaces += get_surfaces(enclosed_area)
            print(f"Enclosed group found starting at {enclosed_cube}")

    print(total_surfaces - enclosed_surfaces)



if __name__ == '__main__':
    solve()
