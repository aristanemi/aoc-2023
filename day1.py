#!/usr/bin/python3
import pandas as pd
import numpy as np
import re

filename="/home/abhi/repos/aoc/inputs/trebuchet_input.txt"
with open(filename) as f:
    lines = [line.rstrip() for line in f]

word2int = {
        'one':'1',
        'two':'2',
        'three':'3',
        'four':'4',
        'five':'5',
        'six':'6',
        'seven':'7',
        'eight':'8',
        'nine':'9'
            }

total = 0
for l in lines:
    df = pd.DataFrame(
        {
            'words':word2int.keys(),
            'id':-1,
            'len':0
        }
    )
    print(l, end=', ')
    temp_l = list(l)
    for w in word2int:
        ids = [m.start() for m in re.finditer(w, l)]
        for id in ids:
            temp_l[id] = word2int[w]
    l = ''.join(temp_l)
    n = ''.join(re.findall(r'\d+', l))
    print(n, end = ', ')
    calib_val = int(n[0])*10 + int(n[-1])
    print(calib_val)
    if len(n):
        total = total + calib_val
print(f'total calibration value = {total}')

