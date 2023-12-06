#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import re
from multiprocessing import  Pool
argc = len(sys.argv)
if argc != 2:
    print("Provide filename of the input")
    quit()

filename = sys.argv[1]
print(f'input used {filename}')

with open(filename) as f:
    lines = [line.rstrip() for line in f]

line_count = len(lines)
boundary = len(lines[0])

seeds_ranges = [int(m) for m in re.findall(r'\d+', lines[0])]
seeds = pd.DataFrame(
    {
        'source':np.zeros(len(seeds_ranges)//2, dtype=int),
        'offset':np.zeros(len(seeds_ranges)//2, dtype=int)
    }
)

for i in range(int(len(seeds_ranges)/2)):
    # print(seeds_ranges)
    seeds.at[i, 'source'] = int(seeds_ranges[i*2])
    seeds.at[i, 'offset'] = int(seeds_ranges[(i*2)+1])
# print(seeds)

maps = []
map_started = False
for i, l in enumerate(lines):
    if 'map' in l:
        map_started = True
        index = 0
        d2s = pd.DataFrame({
            'destination':np.empty( 1, dtype=int),
            'source':np.empty( 1, dtype=int),
            'offset':np.empty( 1, dtype=int)
        })
        continue
    if (len(l)==0 or i == line_count -1) and map_started:
        map_started = False
        maps.append(d2s)
        # print(d2s)

    if map_started:
        numbers = [int(m) for m in re.findall(r'\d+', l)]
        d2s.at[index, 'destination'] = numbers[0]
        d2s.at[index, 'source'] = numbers[1]
        d2s.at[index, 'offset'] = numbers[2]
        index = index + 1

def get_destination(df : pd.DataFrame, s):
    for _, row in df.iterrows():
        start = row['source']
        end = start + row['offset']
        if s >= start and s<= end:
            offset = s - start
            offset_remaining = end -s
            return row['destination']+offset , offset_remaining
    return s, 0

locations = []
new_seeds = []
def get_seeds(seed):
    start = seed[0]
    end = start + seed[1]
    return [s for s in range(start, end + 1)]

def get_mini_loc(seed):
    print(f'working on {seed[0]=}')
    min_loc = 10000000000
    for source in get_seeds(seed):
        # print(source, end= ' ')
        for m in maps:
            dest, _ = get_destination(m, source)
            source = dest
        min_loc = min(dest, min_loc)
        # print(dest, min_loc)
    print(f"{min_loc=} for {seed[0]=}")
    return min_loc

def split_ranges():
    seeds_list=[]
    for _, s in  seeds.iterrows():
        start = s['source']
        offset = s['offset']
        range_size = 10000
        num_ranges = offset // range_size
        last_offset = offset % range_size
        for i in range(num_ranges):
            seeds_list.append((start + i*range_size, range_size))
        seeds_list.append((start + num_ranges*range_size, last_offset))
    return seeds_list

with Pool(processes=6) as pool:
    seeds_list = split_ranges()
    locs = pool.map(get_mini_loc, seeds_list)
    print(min(locs))