from utils import read_lines


def load_data(sample):
    inputs = read_lines(__file__, sample=sample)

    elves_items = []
    elve_items = []
    for calory in inputs:
        if calory != '':
            elve_items.append(int(calory))
        else:
            elves_items.append(elve_items)
            elve_items = []

    elves_items.append(elve_items)
    return elves_items

def solve_part1(elves_items):
    return max([sum(items) for items in elves_items])

def solve_part2(elves_items):
    elves_items = sorted(elves_items, key=sum, reverse=True)
    return sum([sum(items) for items in elves_items[:3]])


if __name__ == '__main__':
    print(solve_part1(load_data(False)))
    print(solve_part2(load_data(False)))
