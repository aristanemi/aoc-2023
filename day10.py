#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import re
from dataclasses import dataclass

with open(sys.argv[1]) as f:
    lines = [line.rstrip() for line in f]

class Tile:
    def __init__(self, val, index):
        self.val =  val
        self.index = index
    def __repr__(self):
        return f' T[{self.index}]={self.val} '

    def __lt__(self, other):
        return self.index < other.index

nr = len(lines)
nc = len(lines[0])
tiles = np.empty(shape=[nr, nc], dtype=Tile)
for r in range(nr):
    for c in range(nc):
        tiles[r,c] = Tile(lines[r][c], (r,c))

n_allowed_tiles = ['|', '7', 'F','S']
s_allowed_tiles = ['|', 'L', 'J','S']
e_allowed_tiles = ['-', 'J', '7','S']
w_allowed_tiles = ['-', 'F', 'L','S']
allowed_tiles = [n_allowed_tiles, s_allowed_tiles, e_allowed_tiles, w_allowed_tiles]

tile_types = {
    '|':[allowed_tiles[count] if val == 1 else []  for count, val in enumerate([1, 1, 0, 0])],
    '-':[allowed_tiles[count] if val == 1 else []  for count, val in enumerate([0, 0, 1, 1])],
    'L':[allowed_tiles[count] if val == 1 else []  for count, val in enumerate([1, 0, 1, 0])],
    'J':[allowed_tiles[count] if val == 1 else []  for count, val in enumerate([1, 0, 0, 1])],
    '7':[allowed_tiles[count] if val == 1 else []  for count, val in enumerate([0, 1, 0, 1])],
    'F':[allowed_tiles[count] if val == 1 else []  for count, val in enumerate([0, 1, 1, 0])],
    '.':[allowed_tiles[count] if val == 1 else []  for count, val in enumerate([0, 0, 0, 0])],
    'S':[allowed_tiles[count] if val == 1 else []  for count, val in enumerate([1, 1, 1, 1])]
}


def print_tiles(tiles: np.ndarray):
    [nr, nc] = tiles.shape
    for r in range(nr):
        for c in range(nc):
            print(tiles[r,c].val, end='')
        print('')

def print_path(path):
    for p in path:
        print(f'{p.val} -> ', end='')
    print('')
    print(f'length of loop {len(path)}')
    print(f'Farthest point of loop {path[len(path)//2]}')

def get_surronded_tiles(index:tuple[int, int]):
    i, j = index[0], index[1]
    n, s, e, w = None, None, None, None
    if i > 0:
        n = tiles[i-1, j]
    if i < (nr - 1):
        s = tiles[i+1, j]
    if j > 0:
        w = tiles[i, j-1]
    if j < (nc - 1):
        e = tiles[i, j + 1]
    return (n, s, e, w)


def get_connected_tiles(t: Tile):
    s_tiles = get_surronded_tiles(t.index)
    # print(t, s_tiles)
    connected = []
    allowed = tile_types.setdefault(t.val, [[],[],[],[]])
    for i, a in enumerate(s_tiles):
        if a is not None and a.val in allowed[i]:
            connected.append(a)
    return connected

def get_next_tile(c_tiles, parent_tile):
    for t in c_tiles:
        if t is parent_tile:
            continue
        return t

# print_tiles(tiles)

# find S
S_tile = None
for t in tiles.ravel():
    if t.val == 'S':
        S_tile = t
        break
print(S_tile)
initial_tiles = get_connected_tiles(S_tile)
print(initial_tiles)

ending_tile = initial_tiles[1]
parent_tile = S_tile
curr_tile = initial_tiles[0]
path = [S_tile, curr_tile]
while True:
    c_tiles = get_connected_tiles(curr_tile)
    if len(c_tiles) != 2 :
        print(f"{curr_tile} has error connections {c_tiles}")
        break
    if ending_tile in c_tiles:
        break
    next_tile = get_next_tile(c_tiles, parent_tile)
    path.append(next_tile)
    parent_tile = curr_tile
    curr_tile = next_tile
path.append(ending_tile)
# print_path(path)

# part 2
path_indices = np.zeros(shape=[nr, nc], dtype=int)
for p in path:
    path_indices[p.index] = 1

inside_nodes = 0

for i, r in enumerate(path_indices[5:6]):
    cols = np.where(r == 1)
    print(cols)
    if len(cols[0]) == 0:
        continue
    pairs=[]
    initial = None
    continuity_detected = False
    for c in cols[0]:
        t = tiles[i, c]
        if initial is None:
            initial = t
            continue
        connected_tiles = get_connected_tiles(t)
        if initial in connected_tiles:
            initial = t
            continuity_detected = True
            continue
        if continuity_detected:
            continuity_detected = False
        else:
            diff = (t.index[1] - initial.index[1] - 1)
            inside_nodes+= diff
            if diff:
                print("Found inside nodes in row ", i, diff)
        initial = None

    
print(f"Number of inside nodes {inside_nodes}")



