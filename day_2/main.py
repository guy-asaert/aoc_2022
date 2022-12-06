from utils import read_lines


shape_score = {
    'A': 1,
    'B': 2,
    'C': 3,
}

my_wins = ('AB', 'BC', 'CA')

map_shape = {'X': 'A', 'Y': 'B', 'Z': 'C'}

win_choice = {'A': 'B', 'B': 'C', 'C': 'A'}
loose_choice = {'A': 'C', 'B': 'A', 'C': 'B'}


def play(part1=True):
    opponent_score = 0
    my_score = 0

    for line in read_lines(__file__, sample=False):
        o, m = line.split(' ')
        if part1:
            m = map_shape[m]
        else:
            if m == 'X': # lose
                m = loose_choice[o]
            elif m == 'Y': # draw
                m = o
            else: # win
                m = win_choice[o]

        opponent_score += shape_score[o]
        my_score += shape_score[m]
        if o == m:
            opponent_score += 3
            my_score += 3
        elif o+m in my_wins: 
            my_score += 6
        else:
            opponent_score += 6

        pass
        
    return opponent_score, my_score


if __name__ == '__main__':
    print(play(False))