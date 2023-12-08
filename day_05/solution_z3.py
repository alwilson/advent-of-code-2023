#!/usr/bin/env python3

from dataclasses import dataclass
from math import prod
import pprint as pp
import z3

@dataclass
class Map:
    map: list
    next_map: str

def parse(file):
    seeds = []
    maps = {}
    with open(file) as fd:
        new_map = []
        map_name = ''
        next_map = ''
        for line in fd:
            line = line.strip()
            split = line.split()
            if len(split) == 0:
                if map_name != '':
                    maps[map_name] = Map(new_map, next_map)
                new_map = []
                map_name = ''
                next_map = ''
            elif split[0] == 'seeds:':
                seeds = [int(i) for i in split[1:]]
            elif split[1] == 'map:':
                name_split = split[0].split('-')
                map_name = name_split[0]
                next_map = name_split[2]
            else:
                new_map.append([int(i) for i in split])
    return seeds, maps

def solve(file):
    seeds, maps = parse(file)

    locations = []
    for s in seeds:
        cur_map = 'seed'
        while cur_map != 'location':
            for m in maps[cur_map].map:
                if s >= m[1] and s < m[1] + m[2]:
                    s += (m[0]-m[1])
                    break
            cur_map = maps[cur_map].next_map

        locations.append(s)

    print(f'Part 1 - {file}: {min(locations)}')

    s = z3.Optimize()
    seed = z3.Int('seed')

    seed_starts = seeds[::2]
    seed_widths = seeds[1::2]
    range_asserts = []
    for seed_start, seed_width in zip(seed_starts, seed_widths):
        range_asserts.append(z3.And(seed >= seed_start, seed < seed_start + seed_width))
    s.add(z3.Or(range_asserts))

    cur_map = 'seed'
    prev_val = seed
    while cur_map != 'location':
        next_map = maps[cur_map].next_map
        val = z3.Int(next_map)
        prev_case = (val == prev_val)
        for m in maps[cur_map].map:
            range = z3.And(prev_val >= m[1], prev_val < m[1] + m[2])
            equality_assert = z3.If(range, val == prev_val + (m[0] - m[1]), prev_case)
            prev_case = equality_assert
        s.add(equality_assert)
        cur_map = maps[cur_map].next_map
        prev_val = val

    location = prev_val
    s.minimize(location)

    ret = s.check()
    if ret == z3.sat:
        m = s.model()
        print(f'Part 2 - {file}: {m[location]}')
    else:
        print(ret)
        exit(-1)

solve('./example.txt')
solve('./input.txt')
