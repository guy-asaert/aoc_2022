from utils import iter_lines, read_lines
import functools


def is_ordered(left, right):

    if isinstance(left, int):
        if isinstance(right, int):
            return left < right
        else:  # list
            return is_ordered([left], right)
    else:
        if isinstance(right, int):
            return is_ordered(left, [right])
        else:
            for i in range(len(left)):
                if i < len(right):
                    if is_ordered(left[i], right[i]):
                        return True
                    elif is_ordered(right[i], left[i]):
                        return False
            return len(left) < len(right)


def part1():
    line_iterator = iter(iter_lines(__file__, '_puzzle.txt'))

    is_ordered_result = []
    try:
        while True:
            left = eval(next(line_iterator))
            right = eval(next(line_iterator))
            is_ordered_result.append(is_ordered(left, right))
            print("{}: {}".format(len(is_ordered_result), is_ordered_result[-1]))

            empty_line = next(line_iterator)

    except StopIteration as _:
        pass
    print('Result: {}'.format(
        sum([i+1 for i in range(len(is_ordered_result)) if is_ordered_result[i]])))


def compare(left, right):

    if isinstance(left, int):
        if isinstance(right, int):
            return left - right
        else:  # list
            return is_ordered([left], right)
    else:
        if isinstance(right, int):
            return is_ordered(left, [right])
        else:
            for i in range(len(left)):
                if i < len(right):
                    if is_ordered(left[i], right[i]):
                        return -1
                    elif is_ordered(right[i], left[i]):
                        return 1
            return len(left) - len(right)


def part2(puzzle_input):
    puzzle_input.append([[2]])
    puzzle_input.append([[6]])

    order_packets = sorted(puzzle_input, key=functools.cmp_to_key(compare))
    return (order_packets.index([[2]]) + 1) *  (order_packets.index([[6]]) + 1)


if __name__ == '__main__':
    # part1()
    puzzle_input = [eval(line) for line in iter_lines(__file__, '_puzzle.txt') if len(line)]
    print(part2(puzzle_input))
