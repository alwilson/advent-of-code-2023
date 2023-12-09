#!/usr/bin/env python3

from dataclasses import dataclass
from math import prod
import pprint as pp
import multiprocessing as mp

@dataclass
class Hand:
    cards: list
    original: str
    score: int

def parse(file):
    hands = []
    with open(file) as fd:
        for line in fd:
            line = line.strip()
            split = line.split()
            hand = split[0]
            # Convert face/ten cards to high ascii to make sorting easier
            hand = hand.replace('T', ':')
            hand = hand.replace('J', ';')
            hand = hand.replace('Q', '<')
            hand = hand.replace('K', '=')
            hand = hand.replace('A', '>')
            hands.append(Hand(hand, split[0], int(split[1])))
    return hands

def solve_p1(file):
    hands = parse(file)

    types = {'five': [], 'four': [], 'three': [], 'two': [], 'one': [], 'full_house': [], 'high': []}
    for h in hands:
        if len(set(h.cards)) == 1:
            types['five'].append(h)
        elif any(h.cards.count(c) == 4 for c in h.cards):
            types['four'].append(h)
        elif any(h.cards.count(c) == 3 for c in h.cards) and any(h.cards.count(c) == 2 for c in h.cards):
            types['full_house'].append(h)
        elif any(h.cards.count(c) == 3 for c in h.cards):
            types['three'].append(h)
        elif len(set(h.cards)) == 3:
            types['two'].append(h)
        elif len(set(h.cards)) == 4:
            types['one'].append(h)
        elif len(set(h.cards)) == 5:
            types['high'].append(h)


    order = ['five', 'four', 'full_house', 'three', 'two', 'one', 'high']

    # Sort each list of hands by the ascii value of cards
    for t in order:
        types[t].sort(key=lambda x: x.cards)

    # for t in order[::-1]:
    #     print(t)
    #     for h in types[t]:
    #         print(h.cards)
    #     print()

    i = 1 
    score = 0
    for t in order[::-1]:
        for h in types[t]:
            # print(f'{i} - {h.cards} - {h.score}')
            score += h.score * i
            i += 1

    print(f'Part 1 - {file}: {score}')

def solve_p2(file):
    hands = parse(file)

    types = {'five': [], 'four': [], 'three': [], 'two': [], 'one': [], 'full_house': [], 'high': []}
    for h in hands:
        num_jokers = h.cards.count(';')
        has_jokers = int(';' in h.cards)
        has_some_jokers = 1 if 5 > num_jokers > 0 else 0
        if len(set(h.cards)) - has_some_jokers == 1:
            types['five'].append(h)
        elif any((h.cards.count(c) + (0 if c == ';' else num_jokers)) == 4 for c in h.cards):
            types['four'].append(h)
        # I think many of these full_house rules are bogus and only 1 joker is possible
        elif any(h.cards.count(c) == 3 for c in h.cards) and any(h.cards.count(c) == 2 for c in h.cards):
            types['full_house'].append(h)
        elif any(h.cards.count(c) == 2 and c != ';' for c in h.cards) and num_jokers == 2:
            types['full_house'].append(h)
        elif any(h.cards.count(c) == 3 and c != ';' for c in h.cards) and num_jokers == 1:
            types['full_house'].append(h)
        elif all((h.cards.count(c) == 2 or c == ';') for c in h.cards) and num_jokers == 1:
            types['full_house'].append(h)
        elif any(h.cards.count(c) == 3 for c in h.cards):
            types['three'].append(h)
        elif any(h.cards.count(c) == 2 for c in h.cards) and num_jokers == 1:
            types['three'].append(h)
        elif num_jokers == 2:
            types['three'].append(h)
        elif len(set(h.cards)) == 3:
            types['two'].append(h)
        elif has_jokers:
            types['one'].append(h)
        elif len(set(h.cards)) == 4:
            types['one'].append(h)
        elif len(set(h.cards)) == 5:
            types['high'].append(h)

    order = ['five', 'four', 'full_house', 'three', 'two', 'one', 'high']

    # Make J the lowest card by turning it into 1
    for t in order:
        for h in types[t]:
            h.cards = h.cards.replace(';', '1')

    # Sort each list of hands by the ascii value of cards
    for t in order:
        types[t].sort(key=lambda x: x.cards)

    # for t in order[::-1]:
    #     print(t)
    #     for h in types[t]:
    #         print(h.original, h.cards)
    #     print()

    i = 1 
    score = 0
    for t in order[::-1]:
        for h in types[t]:
            score += h.score * i
            i += 1

    print(f'Part 2 - {file}: {score}')

solve_p1('./example.txt')
solve_p1('./input.txt')
solve_p2('./example.txt')
solve_p2('./input.txt')