#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys

with open(sys.argv[1]) as f:
    lines = [line.rstrip() for line in f]

time = [ t.strip() for t in lines[0].split()][1:]
distance = [ t.strip() for t in lines[1].split()][1:]

time = [ int(t) for t in time]
distance = [ int(t) for t in distance]

total_ways = 1
for t, d in zip(time, distance):
    stop_val = 0
    unpossible_ways = 0
    possible_ways = t - 1
    for i in range(1, t//2):
        if ((t-i) * i) > d:
            break
        unpossible_ways += 2
    ways = possible_ways - unpossible_ways
    print(ways)
    total_ways *=ways

print(f'{total_ways=}')
    
