import os
import re

from collections import namedtuple

__here__ = os.path.dirname(__file__)

TEST_DATA = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

SlottedLens = namedtuple('SlottedLens', ['label', 'f'])


def holiday_hash(s: str) -> int:
    c = 0
    for ch in s:
        c += ord(ch)
        c *= 17
        c %= 256
    return c


def init_seq(data):
    instructions = data.replace('\n', '').split(',')
    yield sum(map(holiday_hash, instructions))

    hashmap = {i: [] for i in range(256)}

    for inst in instructions:
        if '=' in inst:
            label, num = inst.split('=')
            slot = hashmap[holiday_hash(label)]
            had_lens = False
            for i, sl in enumerate(slot):
                if sl.label == label:
                    slot[i] = SlottedLens(label, int(num))
                    had_lens = True
                    break
            if not had_lens:
                slot.append(SlottedLens(label, int(num)))
        else:
            label = inst.replace('-', '')
            slot = hashmap[holiday_hash(label)]

            for i, sl in enumerate(slot):
                if sl.label == label:
                    del slot[i]
                    break

    # focusing power.
    power = 0
    for sno, slot in hashmap.items():
        for i, sl in enumerate(slot):
            power += (sno + 1) * (i + 1) * sl.f

    yield power

if __name__ == '__main__':
    assert holiday_hash('HASH') == 52
    test_case = init_seq(TEST_DATA)
    assert next(test_case) == 1320
    assert next(test_case) == 145

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = init_seq(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
