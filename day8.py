#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import re

with open(sys.argv[1]) as f:
    lines = [line.rstrip() for line in f]

def encode_rl(c):
    if c == 'R':
        return 1
    if c == 'L':
        return 0
    return ValueError

instructions = list(map(encode_rl, lines[0]))
print(instructions)

nodes = {}
for l in lines[2:]:
    node_names = re.findall(r'[A-Z]{3}', l)
    nodes[node_names[0]] = (node_names[1], node_names[2])

def part1():
    steps = 0
    n = nodes['AAA']
    while True:
        for i in instructions:
            steps += 1
            next_node_name = n[i]
            if next_node_name == 'ZZZ':
                break
            n = nodes[next_node_name]
        if next_node_name == 'ZZZ':
            break
    print(f"Number of {steps=} ")

# part 2

df = pd.DataFrame(
    {
        'name':nodes.keys(),
        'R':'',
        'L':''
    }
)

for i,_ in enumerate(df.iterrows()):
    df.at[i, 'L'] = nodes[df.at[i, 'name']][0]
    df.at[i, 'R'] = nodes[df.at[i, 'name']][1]
df=df.set_index('name')
df_a = df.filter(regex=r'[A-Z]{2}A', axis=0)
count_a = len(df_a)
print(f'{count_a=}')
count_z = 0
steps = 0
instructions = lines[0]
end_match = re.compile(r'[A-Z]{2}Z')
while count_a != count_z:
    for i in instructions:
        steps += 1
        df_a = df.loc[df_a[i].to_list()]
        count_z = len(df_a.filter(regex=r'[A-Z]{2}Z', axis=0))
        if count_z > 0:
            print(f'{count_z=}')
        if count_a == count_z:
            break
        if steps % 10000 == 0:
            print(steps)
        # print(df_a)
        # input()

print(f'number of {steps=}')
