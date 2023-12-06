import os
import re

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''
def parse_data(data):
    for line in data.splitlines():
        a, b = line.split(': ')
        game_id = int(a.split(' ')[1])
        sets = b.split('; ')
        rounds = []
        for s in sets:
            balls = s.split(', ')
            outcome = {'red': 0, 'green': 0, 'blue': 0}
            for ball in balls:
                count, color = ball.split(' ')
                outcome[color] = int(count)
            rounds.append(outcome)
        yield (game_id, rounds)

def gamer_tag(data):
    def is_possible(rounds):
        for r in rounds:
            if r['red'] > 12:
                return False
            if r['green'] > 13:
                return False
            if r['blue'] > 14:
                return False
        return True
    yield sum([game_id for game_id, rounds in parse_data(data) if is_possible(rounds)])

    power_sum = 0
    for game_id, rounds in parse_data(data):
        min_power = 1
        for color in ['red', 'green', 'blue']:
            min_power *= max([r[color] for r in rounds])
        power_sum += min_power
    yield power_sum

if __name__ == '__main__':
    test_case = gamer_tag(TEST_DATA)
    assert next(test_case) == 8
    assert next(test_case) == 2286

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = gamer_tag(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
