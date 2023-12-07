#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import heapq

with open(sys.argv[1]) as f:
    lines = [line.rstrip() for line in f]

labels='J23456789TQKA'

from enum import Enum
class Type(Enum):
    HIGH_CARD=1
    ONE_PAIR=2
    TWO_PAIR=3
    THREE_OF_KIND=4
    FULL_HOUSE=5
    FOUR_OF_KIND=6
    FIVE_OF_KIND=7

class Hand(object):
    def __init__(self, hand: str, bid: int):
        self.hand = hand
        self.bid = bid
        self.strength = identify_strength(hand)

    def __repr__(self):
        return f'Hand: {self.hand} {self.bid} {self.strength.name}'

    def __lt__(self, other):
        if self.strength.value == other.strength.value:
            return compare_same_strength_hands(self.hand, other.hand)
        return self.strength.value < other.strength.value

def identify_strength(handlabels: str):
    if len(handlabels) != 5:
        return ValueError
    labels = [handlabels.count(c) for c in set(handlabels)]
    labels.sort()
    if labels.count(5) == 1:
        return Type.FIVE_OF_KIND
    if labels.count(4) == 1 and labels.count(1) == 1:
        return Type.FOUR_OF_KIND
    if labels.count(2) == 1 and labels.count(3) == 1:
        return Type.FULL_HOUSE
    if labels.count(3) == 1 and labels.count(1) == 2:
        return Type.THREE_OF_KIND
    if labels.count(2) == 2:
        return Type.TWO_PAIR
    if labels.count(2) == 1 and labels.count(1) == 3:
        return Type.ONE_PAIR
    if labels.count(1) == 5:
        return Type.HIGH_CARD
    print(f"Nothing found for {handlabels} {labels}")
    return ValueError

def change_strength_based_on_J(hand: Hand):
    handlabels = hand.hand
    if len(handlabels) != 5:
        return ValueError
    labels = [handlabels.count(c) for c in set(handlabels)]
    labels.sort()
    strength = hand.strength
    j_count = hand.hand.count('J')
    if j_count != 0:
        if strength == Type.FIVE_OF_KIND:
            return Type.FIVE_OF_KIND

        if strength == Type.FOUR_OF_KIND or strength == Type.FULL_HOUSE:
                return Type.FIVE_OF_KIND

        if strength == Type.THREE_OF_KIND:
            return Type.FOUR_OF_KIND

        if strength == Type.TWO_PAIR:
            if j_count == 2:
                return Type.FOUR_OF_KIND
            else:
                return Type.FULL_HOUSE

        if strength == Type.ONE_PAIR:
            return Type.THREE_OF_KIND

        if strength == Type.HIGH_CARD:
            return Type.ONE_PAIR
    else:
        return hand.strength


def compare_same_strength_hands(hand1: str, hand2: str):
    for c1, c2 in zip(hand1, hand2):
        c1 = labels.find(c1)
        c2 = labels.find(c2)
        if c1 == c2:
            continue
        return c1 < c2

hands=[]
for l in lines:
    elems = [e for e in l.split()]
    hands.append(Hand(elems[0], int(elems[1].strip())))

for h in hands:
    h.strength = change_strength_based_on_J(h)

# print(hands)
heapq.heapify(hands)
# print(hands)
score = 0
print(len(hands))
for i, h in enumerate(heapq.nsmallest(len(hands), hands)):
    score += h.bid*(i+1)
    # print({i+1}, h)
print(score)