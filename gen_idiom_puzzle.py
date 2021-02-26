# vi: set ft=python sts=4 ts=4 sw=4 et:

import json
import random

from crossword import Crossword


def load_idioms():
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
    MIN_TTL_IDIOMS = 15
    MAX_TTL_IDIOMS = 20
    MAX_LONG_IDIOMS = 6
    MAX_TTL_WORDS = 67

    ttl_idioms_num = random.randint(MIN_TTL_IDIOMS, MAX_TTL_IDIOMS)
    long_idioms_num = random.randint(3, MAX_LONG_IDIOMS)

    long_idioms_idx = []
    short_idioms_idx = []
    sel_idioms = []
    ttl_words = 0

    flag = 0
    cw_count = {}
    while ttl_words < MAX_TTL_WORDS and \
          (len(long_idioms_idx)<long_idioms_num or \
           len(short_idioms_idx)<(ttl_idioms_num-long_idioms_num)):
        if (flag%2==0) and (len(long_idioms_idx)<long_idioms_num):
            not_find = True
            iter_num = 0
            while not_find and iter_num<1000:
                sel_long_idx = random.randint(0, len(long_idioms)-1)
                if sel_long_idx not in long_idioms_idx:
                    iter_num += 1
                    if len(sel_idioms):
                        cw = [w for w in long_idioms[sel_long_idx][0]
                                if w in sel_idioms[random.randint(0, len(sel_idioms)-1)][0]]
                        _cw = []
                        for w in cw:
                            if (w not in cw_count) or \
                               (w in cw_count and cw_count[w]<3):
                                _cw.append(w)
                        if len(_cw)>1:
                            long_idioms_idx.append(sel_long_idx)
                            sel_idioms.append(long_idioms[sel_long_idx])
                            ttl_words += len(sel_idioms[-1][0])
                            for w in _cw:
                                if w not in cw_count:
                                    cw_count[w] = 0
                                cw_count[w] += 1
                            not_find = False
                            #print(sel_idioms[-1])
                            #print(cw_count)
                    else:
                        long_idioms_idx.append(sel_long_idx)
                        sel_idioms.append(long_idioms[sel_long_idx])
                        ttl_words += len(sel_idioms[-1][0])
                        not_find = False
                        #print(sel_idioms[-1])
                        #print(cw_count)

        if (flag%2==1) and (len(short_idioms_idx)<(ttl_idioms_num-long_idioms_num)):
            not_find = True
            iter_num = 0
            while not_find and iter_num<1000:
                sel_short_idx = random.randint(0, len(short_idioms)-1)
                if sel_short_idx not in short_idioms_idx:
                    iter_num += 1
                    if len(sel_idioms):
                        cw = [w for w in short_idioms[sel_short_idx][0]
                                if w in sel_idioms[random.randint(0, len(sel_idioms)-1)][0]]
                        _cw = []
                        for w in cw:
                            if (w not in cw_count) or \
                               (w in cw_count and cw_count[w]<3):
                                _cw.append(w)
                        if len(_cw)>1:
                            short_idioms_idx.append(sel_short_idx)
                            sel_idioms.append(short_idioms[sel_short_idx])
                            ttl_words += len(sel_idioms[-1][0])
                            for w in _cw:
                                if w not in cw_count:
                                    cw_count[w] = 0
                                cw_count[w] += 1
                            not_find = False
                            #print(sel_idioms[-1])
                            #print(cw_count)

        flag += 1

    print(cw_count)

    #long_idiom_idx = random.sample(range(1, len(long_idioms)), long_idioms_num)
    #short_idiom_idx = random.sample(
    #    range(1, len(short_idioms)),
    #    ttl_idioms_num - long_idioms_num,
    #)

    #sel_idioms = []
    #ttl_words = 0
    #for k in long_idiom_idx:
    #    sel_idioms.append(long_idioms[k])
    #    ttl_words += len(long_idioms[k][0])
    #for k in short_idiom_idx:
    #    if ttl_words>=MAX_TTL_WORDS:
    #        break
    #    sel_idioms.append(short_idioms[k])
    #    ttl_words += len(short_idioms[k][0])

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
        a = Crossword(12, 12, '**', 5000, sel_idioms)
        a.compute_crossword(20, 5)
        if len(a.current_word_list)/len(sel_idioms)>0.4:
            print(a.word_bank())
            print(a.solution())


