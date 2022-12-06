from utils import read_lines


def run(part1=False):

    reconsider = 0
    for line in read_lines(__file__, sample=False):
        pair1, pair2 = line.split(',')
        pair1_lower, pair1_upper = (int(x) for x in pair1.split('-'))
        pair2_lower, pair2_upper = (int(x) for x in pair2.split('-'))
        pair1_sections = set(range(pair1_lower, pair1_upper+1))
        pair2_sections = set(range(pair2_lower, pair2_upper+1))
        if part1:
            if pair1_sections.issubset(pair2_sections) or pair2_sections.issubset(pair1_sections):
                reconsider += 1
        else:
            if pair1_sections.intersection(pair2_sections):
                reconsider += 1

    return reconsider


if __name__ == '__main__':
    print(run(False))
