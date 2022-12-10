from utils import read_lines
from functools import lru_cache
import re


class Folder:
    def __init__(self, name):
        self.name = name
        self.children = dict()

    def find_at_most(self, size_limit, nodes):
        if self.size <= size_limit:
            nodes.append(self)

        for c in self.children.values():
            c.find_at_most(size_limit, nodes)

    @property
    @lru_cache
    def size(self):
        return sum([i.size for i in self.children.values()])


class File:
    def __init__(self, file_size, file_name):
        self.file_size = file_size
        self.file_name = file_name

    def find_at_most(self, size_limit, nodes):
        pass

    @property
    @lru_cache
    def size(self):
        return self.file_size


def process(browsing_lines, current_folder):
    ls_pattern = re.compile(r'\$ ls')
    dir_pattern = re.compile(r'dir ([a-z]*)')
    file_pattern = re.compile(r'(\d*) ([a-z\.]*)')
    cd_pattern = re.compile(r'\$ cd (.*)')

    keep_going = True

    while keep_going:
        if not browsing_lines:
            return browsing_lines
        cd_match = cd_pattern.fullmatch(browsing_lines[0])
        if cd_match:
            folder_name = cd_match.group(1)
            if folder_name == '..':
                return browsing_lines[1:]
            else:
                browsing_lines = process(browsing_lines[1:], current_folder.children[folder_name])
            continue

        ls_match = ls_pattern.fullmatch(browsing_lines[0])
        if ls_match:
            # do not think that we need to do anything
            browsing_lines = browsing_lines[1:]
            continue

        dir_match = dir_pattern.fullmatch(browsing_lines[0])
        if dir_match:
            folder_name = dir_match.group(1)
            current_folder.children[folder_name] = Folder(folder_name)
            browsing_lines = browsing_lines[1:]
            continue

        file_match = file_pattern.fullmatch(browsing_lines[0])
        if file_match:
            file_name = file_match.group(2)
            file_object = File(int(file_match.group(1)), file_name)
            current_folder.children[file_name] = file_object
            browsing_lines = browsing_lines[1:]
            continue

        raise RuntimeError('Cannot parse line {}'.format(browsing_lines[0]))


def puzzle():
    browsing_lines = read_lines(__file__, sample=False)

    root_line = browsing_lines[0]
    assert root_line==r'$ cd /'
    root = Folder('/')
    process(browsing_lines[1:], root)
    results = []
    root.find_at_most(100000, results)
    part1_answer = sum(f.size for f in results)

    unused_space = 70000000 - root.size
    space_needed = 30000000 - unused_space
    all_folders = []
    root.find_at_most(root.size + 1, all_folders)
    all_folders.sort(key=lambda f: f.size)

    smallest_to_delete = 0
    for i in range(len(all_folders)):
        if all_folders[i].size > space_needed:
            smallest_to_delete = all_folders[i].size
            break

    return part1_answer, smallest_to_delete


if __name__ == '__main__':
    print(puzzle())
