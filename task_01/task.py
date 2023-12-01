import os
import re

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
'''

TEST_DATA_2 = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''


def calibration_value(data):
    parse_digits = lambda line: [c for c in line if c.isdigit()]
    combined_value = lambda digits: int(''.join([digits[0], digits[-1]]))
    values = [combined_value(parse_digits(line)) for line in data.splitlines()]
    yield sum(values)

num_words = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}
# Positive lookahead to match overlaps
match_pattern = rf'(?=(\d|{"|".join(num_words.keys())}))'

def calibration_letters(data):
    combined_value = lambda digits: int(''.join([digits[0], digits[-1]]))
    values = []
    for line in data.splitlines():
        elems = re.split(match_pattern, line)
        x = [num_words.get(e, e) for e in elems if e.isdigit() or e in num_words.keys()]
        values.append(combined_value(x))
    yield sum(values)


if __name__ == '__main__':
    test_case = calibration_value(TEST_DATA)
    assert next(test_case) == 142
    test_case = calibration_letters(TEST_DATA_2)
    assert next(test_case) == 281

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = calibration_value(data)
    print(f'answer_1={next(answers)}')
    answers = calibration_letters(data)
    print(f'answer_2={next(answers)}')
