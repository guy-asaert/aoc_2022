from utils import read_lines
import re


MATCH_MOTION = r'(\w) (\d+)'

STEPS = {
    'R': [1, 0],
    'D': [0, -1],
    'L': [-1, 0],
    'U': [0, 1],
}

KNOTS = 10


def part1():
    match_motion = re.compile(MATCH_MOTION)

    rope = [[0, 0] for i in range(KNOTS)]
    # head_position = [0, 0]
    # tail_position = [0, 0]
    tail_location_visited = set()

    for motion in read_lines(__file__, sample=False):
        result = match_motion.match(motion)
        direction = result.group(1)
        steps = int(result.group(2))
        for i in range(steps):
            rope[0] = [
                rope[0][0] + STEPS[direction][0],
                rope[0][1] + STEPS[direction][1],
            ]

            for i in range(1, len(rope)):
                if abs(rope[i-1][0] - rope[i][0]) > 1 or \
                   abs(rope[i-1][1] - rope[i][1]) > 1:
                    if rope[i-1][0] < rope[i][0]:
                        rope[i][0] -= 1
                    if rope[i-1][0] > rope[i][0]:
                        rope[i][0] += 1
                    if rope[i-1][1] < rope[i][1]:
                        rope[i][1] -= 1
                    if rope[i-1][1] > rope[i][1]:
                        rope[i][1] += 1
            tail_location_visited.add(tuple(rope[-1]))

    return len(tail_location_visited)


if __name__ == '__main__':
    print(part1())
