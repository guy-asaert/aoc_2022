from utils import read_lines


class Tree:
    def __init__(self, height):
        self.height = height


def visible(trees):
    ref_height = -1
    visible_trees = []
    for tree in trees:
        if tree.height > ref_height:
            visible_trees.append(tree)
            ref_height = tree.height

    return visible_trees


def part1():
    trees_file = read_lines(__file__, sample=True)

    trees = []
    for row in trees_file:
        trees.append([Tree(int(x)) for x in row])

    #  rows
    visible_trees = []
    for tree_row in trees:
        visible_trees.extend(visible(tree_row))
        visible_trees.extend(visible(reversed(tree_row)))

    # columns
    for tree_column in zip(*trees):
        visible_trees.extend(visible(tree_column))
        visible_trees.extend(visible(reversed(tree_column)))

    visible_trees = len(set(visible_trees))
    return visible_trees


def part2():
    trees_file = read_lines(__file__, sample=False)

    trees = []
    for row in trees_file:
        trees.append([Tree(int(x)) for x in row])

    highest_scenic_score = 0

    for row in range(len(trees)):
        for column in range(len(trees[row])):
            # left
            left_scenic_score = 0
            if column > 0:
                for local_column in range(column - 1, -1, -1):
                    if trees[row][local_column].height >= trees[row][column].height:
                        left_scenic_score += 1
                        break
                    left_scenic_score += 1

            # right
            right_scenic_score = 0
            if column < len(trees[row]) - 1:
                for local_column in range(column + 1, len(trees[row])):
                    if trees[row][local_column].height >= trees[row][column].height:
                        right_scenic_score += 1
                        break
                    right_scenic_score += 1

            # top
            top_scenic_score = 0
            if row > 0:
                for local_row in range(row - 1, -1, -1):
                    if trees[local_row][column].height >= trees[row][column].height:
                        top_scenic_score += 1
                        break
                    top_scenic_score += 1

            # bottom
            bottom_scenic_score = 0
            if row < len(trees) - 1:
                for local_row in range(row + 1, len(trees)):
                    if trees[local_row][column].height >= trees[row][column].height:
                        bottom_scenic_score += 1
                        break
                    bottom_scenic_score += 1

            highest_scenic_score = max(
                highest_scenic_score,
                left_scenic_score * right_scenic_score * top_scenic_score * bottom_scenic_score)

    return highest_scenic_score


if __name__ == '__main__':
    print(part1())
    print(part2())
