from utils import read_lines

CODE_LENGTH = 14


def part1():
    code = read_lines(__file__, sample=False)[0]

    for i in range(len(code) - CODE_LENGTH):
        if len(set(code[i:i+CODE_LENGTH])) == CODE_LENGTH:
            return i + CODE_LENGTH

    raise RuntimeError("Could not find the marker")


if __name__ == '__main__':
    print(part1())
