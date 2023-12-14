#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import re
from dataclasses import dataclass
import itertools

with open(sys.argv[1]) as f:
    lines = [line.rstrip() for line in f]

class Tile:
    def __init__(self, val, index):
        self.val =  val
        self.index = index
    def __repr__(self):
        return f'{self.val}'

    def __lt__(self, other):
        return self.index < other.index

nr = len(lines)
nc = len(lines[0])
tiles = np.empty(shape=[nr, nc], dtype=str)
for r in range(nr):
    for c in range(nc):
        tiles[r,c] = lines[r][c]

col_ids = []
for i, col in enumerate(np.transpose(tiles)):
    res = np.where(col == '#')
    # print(res)
    if len(res[0]) == 0:
        col_ids.append(i)
row_ids = []
for i, row in enumerate(tiles):
    res = np.where(row == '#')
    # print(res)
    if len(res[0]) == 0:
        row_ids.append(i)

galaxies = np.column_stack(np.where(tiles == '#'))
ef = 1000000
print(galaxies)
print(col_ids)
for count,id in enumerate(col_ids):
    count = count * (ef - 1)
    galaxies = [(g[0], g[1]+ef - 1) if g[1] > (id+count) else (g[0], g[1]) for g in galaxies]

print(row_ids)
for count, id in enumerate(row_ids):
    count = count * (ef - 1)
    galaxies = [(g[0]+ef - 1, g[1]) if g[0] > (id+count) else (g[0], g[1]) for g in galaxies]

print(galaxies)
combinations=list(itertools.combinations(galaxies, 2))
sum_distances = 0
for g1,g2 in combinations:
    sum_distances += (abs(g1[0] - g2[0] ) + abs(g1[1] - g2[1]))
print(sum_distances)