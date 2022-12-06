from utils import read_lines


def part1():

    priority_sum = 0
    for line in read_lines(__file__, sample=False):
        first = line[:len(line)//2]
        second = line[len(line)//2:]
        in_both = set(first).intersection(set(second))
        code = list(in_both)[0]
        if ord(code) >= 97:
            priority = ord(code) - ord('a') + 1
        else:
            priority = ord(code) - ord('A') + 27
        priority_sum += priority
    return priority_sum


def part2():

    priority_sum = 0
    lines = read_lines(__file__, sample=False)
    for index in range(0, len(lines), 3):
        first = lines[index]
        second = lines[index+1]
        third = lines[index+2]

        in_three = set(first).intersection(set(second).intersection(third))
        code = list(in_three)[0]
        if ord(code) >= 97:
            priority = ord(code) - ord('a') + 1
        else:
            priority = ord(code) - ord('A') + 27
        priority_sum += priority
    return priority_sum


if __name__ == '__main__':
    print(part2())
