# vi: set ft=python sts=4 ts=4 sw=4 et:

import json
import random
from math import sqrt

from crossword import Crossword


def load_idioms():
    """Load idiom dataset."""
    with open('idiom.json') as f:
        idiom_set = json.load(f)
    # select idioms
    short_idioms = []
    long_idioms = []
    for item in idiom_set:
        l = len(item['word'])
        if l>4 and l<=10:
            long_idioms.append((item['word'], item['explanation']))
        elif l<=4:
            short_idioms.append((item['word'], item['explanation']))

    return long_idioms, short_idioms

def select_idioms(long_idioms, short_idioms):
    """Get idiom set randomly."""
    MIN_TTL_IDIOMS = 15
    MAX_TTL_IDIOMS = 20
    MIN_LONG_IDIOMS = 2
    MAX_LONG_IDIOMS = 6
    MAX_TTL_WORDS = 67

    # set the number of selected idioms randomly
    ttl_idioms_num = random.randint(MIN_TTL_IDIOMS, MAX_TTL_IDIOMS)
    long_idioms_num = random.randint(MIN_LONG_IDIOMS, MAX_LONG_IDIOMS)
    short_idioms_num = ttl_idioms_num - long_idioms_num

    long_idioms_idx = []
    short_idioms_idx = []
    sel_idioms = []
    ttl_words = 0

    _flag = -1
    interset_count = {}
    while ttl_words < MAX_TTL_WORDS and \
          (len(long_idioms_idx) < long_idioms_num or \
           len(short_idioms_idx) < short_idioms_num):
        # select idiom from long- or short-idiom set
        _flag += 1
        if (_flag%2 == 0) and (len(long_idioms_idx) < long_idioms_num):
            # select idiom from long-set
            _idiom_set = long_idioms
            _idiom_idx = long_idioms_idx
        elif (_flag%2 == 1) and (len(short_idioms_idx) < short_idioms_num):
            # select idiom from short-set
            _idiom_set = short_idioms
            _idiom_idx = short_idioms_idx
        else:
            continue

        # select idiom from the specified idiom set
        not_find = True
        iter_num = 0
        while not_find and iter_num<1000:
            sel_idx = random.randint(0, len(_idiom_set)-1)
            if sel_idx not in _idiom_idx:
                iter_num += 1
                if len(sel_idioms):
                    ref_idx = random.randint(0, len(sel_idioms)-1)
                    _max_interset = int(sqrt(len(sel_idioms[ref_idx][0]))+0.5)
                    if interset_count[ref_idx] < _max_interset:
                        _cw = [
                            w for w in _idiom_set[sel_idx][0]
                                if w in sel_idioms[ref_idx][0]
                        ]
                        if len(_cw)==2:
                            _idiom_idx.append(sel_idx)
                            sel_idioms.append(_idiom_set[sel_idx])
                            ttl_words += len(sel_idioms[-1][0])
                            interset_count[ref_idx] += 1
                            interset_count[len(sel_idioms)-1] = 1
                            not_find = False
                            #print(sel_idioms[-1])
                            #print(interset_count)
                else:
                    _idiom_idx.append(sel_idx)
                    sel_idioms.append(_idiom_set[sel_idx])
                    ttl_words += len(sel_idioms[-1][0])
                    interset_count[0] = 0
                    not_find = False
                    #print(sel_idioms[-1])
                    #print(interset_count)

    print(interset_count)

    return sel_idioms


if __name__ == '__main__':
    # load idiom dataset
    long_idioms, short_idioms = load_idioms()

    for _ in range(10000):
        # select idioms randomly
        sel_idioms = select_idioms(long_idioms, short_idioms)
        print('Select idioms:')
        for item in sel_idioms:
            print(item)
        print('\n')

        # generate puzzle
        a = Crossword(11, 11, '**', 5000, sel_idioms)
        a.compute_crossword(30, 2)
        if len(a.current_word_list)/len(sel_idioms)>0.4:
            print(a.word_bank())
            print(a.solution())
            #print(a.display())
            print(a.legend())


