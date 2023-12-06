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

num_games = len(lines)
df = pd.DataFrame(
    {
        'id' : np.arange(0, num_games, dtype=int)+1,
        'red': np.zeros(num_games, dtype=int),
        'green': np.zeros(num_games, dtype=int),
        'blue': np.zeros(num_games, dtype=int)
    }
)

power_of_set = 0
for i, l in enumerate(lines):
    for c in ['red', 'green', 'blue']:
        num_cubes = [int(re.match(r'\d+', m).group(0)) for m in re.findall(r'\d+ '+c, l)]
        df.at[i, c] = max(num_cubes)
    df_part1 = df[(df['red'] <= 12) & (df['green'] <= 13) & (df['blue'] <= 14)]
    power_of_set = power_of_set + (df['red'][i] * df['green'][i] * df['blue'][i])

print(df_part1['id'].sum())
print(f'{power_of_set=}')
