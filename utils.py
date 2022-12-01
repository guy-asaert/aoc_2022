import os

def read_lines(code_file, sample=False, conversion=None):
    with open(os.path.join(os.path.dirname(code_file), "sample.txt" if sample else "input.txt"), 'r') as f:
        return [conversion(line) if conversion else line for line in f.read().splitlines()]
