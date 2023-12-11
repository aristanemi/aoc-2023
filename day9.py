#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import re

with open(sys.argv[1]) as f:
    lines = [line.rstrip() for line in f]

history=[]
for l in lines:
    a = [int(n) for n in l.split()]
    history.append(a)

for h in history:
    first_elem = h[0]
    next_elem = h[-1]
    t = h
    i = 1
    while t[-1] != 0:
        # print(t, i)
        t = np.diff(h,n=i)
        next_elem += t[-1]
        first_elem += (t[0] * pow(-1, i))
        i += 1
    h.append(next_elem)
    h.insert(0, first_elem)

cum_sum = 0
for h in history:
    cum_sum += h[-1]
print(f"Cumulative sum part(1) is {cum_sum}")

cum_sum=0
for h in history:
    cum_sum += h[0]

print(f"Cumulative sum part(2) is {cum_sum}")

