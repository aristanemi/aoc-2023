#!/usr/bin/python3
import pandas as pd
import numpy as np

filename="/home/abhi/repos/aoc/inputs/scratchcards_input.txt"
with open(filename) as f:
    lines = [line.rstrip() for line in f]


def get_matching_count(l):
    _,_,all_numbers = l.partition(":")
    winning,_,you_have = all_numbers.partition("|")
    all_numbers = winning.strip().replace('  ', ' ').split(' ') + you_have.strip().replace('  ', ' ').split(' ')
    complete_count = len(all_numbers) # total count of winning + you_have numbers
    get_matching_count = complete_count - len(set(all_numbers))
    return  get_matching_count

def get_points(num_matching):
    if num_matching:
        return pow(2, num_matching - 1)
    else:
        return 0

total_points = 0
for l in lines:
    total_points = total_points + get_points(get_matching_count(l))
print(f'{total_points=}')

# part two -> find number of cards which will we end up with
cards_points = pd.DataFrame({
    'index':np.arange(len(lines)),
    'count':1,
    'points':0
})

for i, l in enumerate(lines):
    points = cards_points['points'][i] = get_matching_count(l)
    count = cards_points['count'][i]
    if points == 0:
        continue
    for j in range(i+1, points+i+1):
        cards_points['count'][j] = cards_points['count'][j] + count
print(f"{cards_points['count'].sum()}")