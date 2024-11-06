from dataclasses import dataclass
from utils import iter_lines

PUZZLE_INPUT_SAMPLE = '''1
2
-3
3
-2
0
4'''

@dataclass
class PuzzleData:
    offset: int
    processed: bool = False

    def __repr__(self):
        return f'{self.offset}'

def run():
    
    DECRYPTION_KEY = 1
    print(PUZZLE_INPUT_SAMPLE)
    # data = [PuzzleData(int(x) * DECRYPTION_KEY) for x in PUZZLE_INPUT_SAMPLE.split()]
    data = [PuzzleData(int(x)) for x in iter_lines(__file__, '_puzzle.txt')]

    mix_order = [dd.offset for dd in data]
    for i in range(1):
        for item in data:
            item.processed = False

        position = 0
        while position < len(data):
            if data[position].offset != 0:
                data_item = data.pop(position)
                new_location = (position + data_item.offset) % len(data)

                if new_location == 0: # if moved to the front then send to the back
                    new_location = len(data)
                data[new_location:new_location] = [PuzzleData(data_item.offset, True)]
            else:
                data[position].processed = True

            while position < len(data) and data[position].processed:
                position += 1
            pass
        pass

    print(data)
    zero_position = data.index(PuzzleData(0, True))
    thousendth = data[(zero_position + 1000) % len(data)]
    two_thousendth = data[(zero_position + 2000) % len(data)]
    three_thousendth = data[(zero_position + 3000) % len(data)]
    print(f'Gove coordinates: {thousendth.offset + two_thousendth.offset + three_thousendth.offset}')

if __name__ == "__main__":
    run()
