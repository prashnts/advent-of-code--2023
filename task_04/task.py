import os
import re

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''

def parse(data):
    norm = lambda x: {int(y) for y in x.split(' ') if y}
    for line in data.splitlines():
        card, nums = line.split(':')
        wins, mine = nums.split('|')
        yield norm(wins), norm(mine)

def jackpot(data):
    luck = 0
    for wins, mine in parse(data):
        match = wins.intersection(mine)
        if match:
            luck += 2 ** (len(match) - 1)
    yield luck
    yield 0
        


if __name__ == '__main__':
    test_case = jackpot(TEST_DATA)
    assert next(test_case) == 13
    assert next(test_case) == 0

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = jackpot(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
