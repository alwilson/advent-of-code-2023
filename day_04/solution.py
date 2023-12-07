#!/usr/bin/env python3

from dataclasses import dataclass
from math import prod

@dataclass
class ScratchCard:
    wins: list
    nums: list

def parse(file):
    cards = []
    with open(file) as fd:
        for line in fd:
            line = line.strip().split(':')[1]
            split = line.split('|')
            wins = [int(x) for x in split[0].split()]
            nums = [int(x) for x in split[1].split()]
            cards.append(ScratchCard(wins, nums))
    return cards

def solve(file):
    cards = parse(file)

    score = 0
    for c in cards:
        num_matches = len(set(c.wins).intersection(set(c.nums)))
        score += 2**(num_matches-1) if num_matches > 0 else 0

    print(f'Part 1 - {file}: {score}')

    cards_won = {}
    last_card = len(cards)
    for ci, c in enumerate(cards, 1):
        cards_won[ci] = 1
    for ci, c in enumerate(cards, 1):
        num_matches = len(set(c.wins).intersection(set(c.nums)))
        card_multiplier = cards_won[ci]
        for x in range(num_matches):
            xi = ci+x+1
            if xi > last_card:
                break
            cards_won[xi] += card_multiplier

    print(f'Part 2 - {file}: {sum(cards_won.values())}')

solve('./example.txt')
solve('./input.txt')
