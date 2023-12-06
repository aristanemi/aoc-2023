#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import re

argc = len(sys.argv)
if argc != 2:
    print("Provide filename of the input")
    quit()

filename = sys.argv[1]
print(f'input used {filename}')

with open(filename) as f:
    lines = [line.rstrip() for line in f]

line_count = len(lines)
total = 0
for line_num, l in enumerate(lines):
    matches = [m for m in re.finditer(r'\d+', l)]
    boundary = len(l)
    for m in matches:
        search_str = ''
        start = m.start()
        end = m.end()
        if end < boundary:
            end = end + 1
        if start > 0:
            start = start -1
        search_str = search_str + l[start:end] #current line
        if line_num > 0:
            search_str = search_str + lines[line_num - 1][start:end]
        if line_num < (line_count - 1):
            search_str = search_str + lines[line_num + 1][start:end]
        
        if symbol_match := re.search(r'[^\d\.]', search_str):
            # print(symbol_match[0], m[0])
            total = total + int(m[0])
print(total)

gear_ratio = 0
for line_num, l in enumerate(lines):
    matches = [m for m in re.finditer(r'\*', l)]
    boundary = len(l)
    for m in matches:
        start = m.start()
        end = m.end() - 1
        if end < boundary:
            end = end + 1
        if start > 0:
            start = start -1

        digit_matches = []
        digit_matches = digit_matches +  [m for m in re.finditer(r'\d+', l)]
        if line_num > 0:
            search_str = lines[line_num - 1]
            digit_matches = digit_matches +  [m for m in re.finditer(r'\d+', search_str)]
        if line_num < (line_count - 1):
            search_str = lines[line_num + 1]
            digit_matches = digit_matches +  [m for m in re.finditer(r'\d+', search_str)]
        # print(f'symbol {start=},{end=}')
        adjacent_numbers=[]
        for dm in digit_matches:
            dm_start,dm_end = dm.span()
            ids = list(range(dm_start, dm_end))
            # print(ids)
            if start in ids or end in ids:
                adjacent_numbers.append(int(dm[0]))
        if len(adjacent_numbers) == 2:
            gear_ratio = gear_ratio + np.prod(adjacent_numbers)
        
print(f'{gear_ratio=}')


    

