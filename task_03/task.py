import os
import re
import operator

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''


def schematics_detective(data):
    # A number is not a part number if all its neighbors are . or nothing.
    lines = data.splitlines()
    width = len(lines[0])
    height = len(lines)

    def neighbors(lno, span):
        a, b = span
        for l in [lno - 1, lno + 1]:
            if l < 0 or l == height:
                continue
            for x in range(a - 1, b + 1):
                if 0 <= x < width:
                    yield lines[l][x]
        for x in [a - 1, b]:
            if 0 <= x < width:
                yield lines[lno][x]

    def has_symbol(niter):
        for n in niter:
            if n != '.' and not n.isdigit():
                return True

    accum = 0

    for lno, line in enumerate(lines):
        # find all numbers in this line.
        for num in re.finditer(r'\d+', line):
            if has_symbol(neighbors(lno, num.span())):
                accum += int(num.group())

    yield accum

    # Previous solution is not well adapted for part 2, but is in rigit direction.

    def neighbors(lno, pos):
        # here we go again!
        coords = [
            (lno - 1, pos - 1),
            (lno - 1, pos),
            (lno - 1, pos + 1),
            (lno, pos - 1),
            (lno, pos + 1),
            (lno + 1, pos - 1),
            (lno + 1, pos),
            (lno + 1, pos + 1),
        ]
        visited = []
        for l, p in coords:
            if 0 <= l < height and 0 <= p < width:
                for num in re.finditer(r'\d+', lines[l]):
                    a, b = num.span()
                    if a <= p < b:
                        yield int(num.group())

    total_gear_ratios = 0
    for lno, line in enumerate(lines):
        for pos, c in enumerate(line):
            if c == '*':
                ns = set(neighbors(lno, pos))
                if len(ns) == 2:
                    total_gear_ratios += operator.mul(*ns)
    yield total_gear_ratios



if __name__ == '__main__':
    test_case = schematics_detective(TEST_DATA)
    assert next(test_case) == 4361
    assert next(test_case) == 467835

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = schematics_detective(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
