import re
import math
from functools import partial
from utils import iter_lines


RE_MONKEY = r'^Monkey (\d+)'
RE_ITEMS = r'(\d+)'
RE_OPERATION = r'  Operation: (\w+) = (\w+) (.) (\w+)'
RE_TEST = r'  Test: divisible by (\d+)'
RE_THROW = r'    If (\w+): throw to monkey (\d+)'


def add(a, b):
    return a + b


def mult(a, b):
    return a * b


def square(a):
    return a * a


class Monkey:
    def __init__(self):
        self._items = []
        self._operation = None
        self._divisible_number = None
        self._true_monkey = None
        self._false_monkey = None
        self._inspected = 0

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        self._items = new_items

    @property
    def operation(self):
        return self._operation

    @property
    def divisible_number(self):
        return self._divisible_number

    @property
    def true_monkey(self):
        return self._true_monkey

    @property
    def false_monkey(self):
        return self._false_monkey

    @property
    def inspected(self):
        return self._inspected

    @inspected.setter
    def inspected(self, new_inspected):
        self._inspected = new_inspected


def part1():
    re_monkey = re.compile(RE_MONKEY)
    re_items = re.compile(RE_ITEMS)
    re_operation = re.compile(RE_OPERATION)
    re_test = re.compile(RE_TEST)
    re_throw = re.compile(RE_THROW)

    monkeys = []
    new_monkey = None
    for line in iter_lines(__file__, '_puzzle.txt'):
        if re_monkey.match(line):
            if new_monkey:
                monkeys.append(new_monkey)
            new_monkey = Monkey()
        elif 'Starting' in line:
            items = re_items.findall(line)
            new_monkey._items = [int(i) for i in items]
        elif 'Operation' in line:
            operation = re_operation.match(line)
            if operation.group(3) == '+':
                new_monkey._operation = partial(add, int(operation.group(4)))
            elif operation.group(3) == '*':
                if operation.group(4) == 'old':
                    new_monkey._operation = square
                else:
                    new_monkey._operation = partial(mult, int(operation.group(4)))
        elif 'Test' in line:
            test = re_test.match(line)
            new_monkey._divisible_number = int(test.group(1))
        elif 'throw to' in line:
            throw_to = re_throw.match(line)
            if throw_to.group(1) == 'true':
                new_monkey._true_monkey = int(throw_to.group(2))
            else:
                new_monkey._false_monkey = int(throw_to.group(2))

    if new_monkey:
        monkeys.append(new_monkey)

    common_divisible = math.prod([m.divisible_number for m in monkeys])

    for i in range(10000):
        for m in monkeys:
            for item in m.items:
                item = m.operation(item)
                if False:
                    item //= 3
                else:
                    item %= common_divisible

                if item % m.divisible_number == 0:
                    monkeys[m.true_monkey].items.append(item)
                else:
                    monkeys[m.false_monkey].items.append(item)
                m.inspected += 1
            m.items = []

        if i == 999:
            pass

    inspected_items = [m.inspected for m in monkeys]
    inspected_items.sort(reverse=True)
    return inspected_items[0] * inspected_items[1]


if __name__ == '__main__':
    print(part1())
