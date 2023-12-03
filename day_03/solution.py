#!/usr/bin/env python3

from dataclasses import dataclass
from math import prod

def parse(file):
    coords = {}
    symbols = {}
    with open(file) as fd:
        y = 0
        for line in fd:
            line = line.strip()
            num_start = False
            num = 0
            x = 0
            num_x = 0
            num_len = 0
            for c in line:
                if c.isnumeric():
                    if not num_start:
                        num_start = True
                        num = 0
                        num_len = 0
                        num_x = x
                    num = num*10 + int(c)
                    num_len += 1
                else:
                    if c != '.':
                        symbols[(x,y)] = c
                    if num_start:
                        num_start = False
                        for l in range(num_x, num_x+num_len):
                            coords[(l,y)] = ((num_x,y), num)
                        num = 0
                        num_len = 0
                x += 1
            if num_start:
                num_start = False
                for l in range(num_x, num_x+num_len):
                    coords[(l,y)] = ((num_x,y), num)
                num = 0
                num_len = 0
            y += 1

    return coords, symbols

def solve(file):
    coords, symbols = parse(file)

    good_parts = []
    gear_ratios = []
    for sx, sy in symbols:
        local_parts = {}
        lo = [(-1,1),  (0,1),  (1,1),
              (-1,0),          (1,0),
              (-1,-1), (0,-1), (1,-1)]
        for sxo, syo in lo:
            sc = (sx+sxo, sy+syo)
            if sc in coords:
                part = coords[sc]
                local_parts[part[0]] = part[1]

        for part in local_parts.values():
            good_parts.append(part)

        if symbols[(sx,sy)] == '*' and len(local_parts.keys()) == 2:
            gear_ratio = prod(local_parts.values())
            gear_ratios.append(gear_ratio)
            continue

    print(f'Part 1 - {file}: {sum(good_parts)}')
    print(f'Part 2 - {file}: {sum(gear_ratios)}')


solve('./example.txt')
solve('./input.txt')
