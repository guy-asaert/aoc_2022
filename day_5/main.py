from utils import read_lines
from collections import defaultdict
import re


def run(part1=False):
    stacks = defaultdict(list)
    lines = read_lines(__file__, False)
    for line_no, line in enumerate(lines):
        if not line:  # done with stacks
            break
        for i in range(0, len(line), 4):
            stack_element = line[i+1]
            if stack_element != ' ' and re.match('[A-Z]', stack_element):
                stacks[i//4+1].append(stack_element)

    for k, v in stacks.items():
        stacks[k].reverse()

    for line in lines[line_no+1:]:
        result = re.search(r"\bmove (\d+) from (\d+) to (\d+)", line)
        move = int(result.group(1))
        from_stack = int(result.group(2))
        to_stack = int(result.group(3))

        if part1:
            for i in range(move):
                crate = stacks[from_stack].pop()
                stacks[to_stack].append(crate)
        else:
            stacks[to_stack].extend(stacks[from_stack][-move:])
            stacks[from_stack][-move:] = []

    message = ""
    for i in range(len(stacks)):
        message += stacks[i+1][-1]
    return message


if __name__ == '__main__':
    print(run())

